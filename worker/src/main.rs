extern crate futures;
type Pool = diesel::r2d2::Pool<diesel::r2d2::ConnectionManager<diesel::pg::PgConnection>>;

use diesel::prelude::*;
enum TaskRepr {
    AssignUser(i32, i32),
}

async fn handle_task(pool: Pool, task: TaskRepr) {
    let house_items: Vec<(data::House, (data::Task, (data::UserTask, data::User)))> = match task {
        TaskRepr::AssignUser(house_id, _) => match data::schema::house::dsl::house
            .find(house_id)
            .inner_join(data::schema::task::dsl::task.inner_join(
                data::schema::user_task::dsl::user_task.inner_join(data::schema::user::dsl::user),
            ))
            .load::<(data::House, (data::Task, (data::UserTask, data::User)))>(&pool.get().unwrap())
        {
            Ok(t) => t,
            Err(e) => {
                println!("ERROR: {:?}", e);
                return;
            }
        },
        _ => return,
    };
    let mut user_items: std::collections::HashMap<i32, i32> = std::collections::HashMap::new();
    for item in house_items {
        if user_items.contains_key(&((item.1).1).1.id) {
            user_items
                .get_mut(&((item.1).1).1.id)
                .unwrap()
                .checked_add(1)
                .unwrap();
        } else {
            user_items.insert(((item.1).1).1.id, 1);
        }
    }
    let smallest_user = user_items
        .iter()
        .fold((0, 0), |state, (user_id, task_count)| {
            if state.1 > *task_count {
                (*user_id, *task_count)
            } else {
                state
            }
        });
    let (_, task_id) = match task {
        TaskRepr::AssignUser(i1, i2) => (i1, i2),
    };
    match diesel::insert_into(data::schema::user_task::dsl::user_task)
        .values(data::NewUserTask {
            task_id,
            user_id: smallest_user.0,
            done: false,
            deadline: (chrono::Utc::now().naive_utc().timestamp()
                + data::schema::task::dsl::task
                    .find(task_id)
                    .first::<data::Task>(&pool.get().unwrap())
                    .unwrap()
                    .frequency as i64) as i32,
        })
        .execute(&pool.get().unwrap())
    {
        Ok(_) => {}
        Err(e) => {
            println!("ERROR: {:?}", e);
            return;
        }
    };
}

#[tokio::main]
async fn main() {
    let pool: Pool = diesel::r2d2::Pool::builder()
        .build(
            diesel::r2d2::ConnectionManager::<diesel::PgConnection>::new(
                std::env::var("DATABASE_URL").unwrap_or("postgres://localhost".to_string()),
            ),
        )
        .expect("Couldn't create database pool.");
    let mut delay = tokio::time::DelayQueue::<TaskRepr>::new();
    loop {
        async {
            use futures::StreamExt;
            while let Some(n) = delay.next().await {
                match n {
                    Ok(next_task) => {
                        tokio::spawn(handle_task(pool.clone(), next_task.into_inner()));
                    }
                    Err(e) => println!("ERROR: {:?}", e),
                }
            }
            tokio::time::delay_for(tokio::time::Duration::from_secs(30)).await;
            match data::schema::worker_task::dsl::worker_task
                .load::<data::WorkerTask>(&pool.get().unwrap())
            {
                Ok(task_list) => {
                    for item in task_list {
                        match item.task_type {
                            1 => {
                                let mut split_string = item.context.split(',');
                                let house_id = split_string.next().unwrap().parse::<i32>().unwrap();
                                let task_id = split_string.next().unwrap().parse::<i32>().unwrap();
                                delay.insert_at(
                                    TaskRepr::AssignUser(house_id, task_id),
                                    tokio::time::Instant::from_std(
                                        std::time::Instant::now()
                                            + std::time::Duration::from_secs_f64(
                                                item.complete_at.timestamp() as f64,
                                            )
                                            .checked_sub(
                                                std::time::SystemTime::now()
                                                    .duration_since(std::time::UNIX_EPOCH)
                                                    .expect("Time seems to have gone backwards."),
                                            )
                                            .unwrap(),
                                    ),
                                );
                            }
                            _ => println!("ERROR: {} is an invalid task type", item.task_type),
                        }
                    }
                }
                Err(e) => println!("ERROR: {:?}", e),
            }
        }
        .await;
    }
}
