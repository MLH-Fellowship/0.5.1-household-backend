extern crate futures;
type Pool = diesel::r2d2::Pool<diesel::r2d2::ConnectionManager<diesel::pg::PgConnection>>;

use diesel::prelude::*;
enum TaskRepr {
    AssignUser(i32),
}

async fn handle_task(conn: Pool, task: TaskRepr) {}

#[tokio::main]
async fn main() {
    let pool: Pool = diesel::r2d2::Pool::builder()
        .build(
            diesel::r2d2::ConnectionManager::<diesel::PgConnection>::new(
                std::env::var("DATABASE_URL").unwrap_or("postgres://localhost".to_string()),
            ),
        )
        .expect("Couldn't create database pool.");
    let rt = tokio::runtime::Runtime::new().unwrap();
    let mut delay = tokio::time::DelayQueue::<TaskRepr>::new();
    loop {
        async {
            use futures::StreamExt;
            if let Some(n) = delay.next().await {
                match n {
                    Ok(next_task) => {
                        tokio::spawn(handle_task(pool.clone(), next_task.into_inner()));
                    }
                    Err(e) => println!("ERROR: {:?}", e),
                }
            };
            tokio::time::delay_for(tokio::time::Duration::from_secs(30)).await;
            match data::schema::worker_task::dsl::worker_task
                .load::<data::WorkerTask>(&pool.get().unwrap())
            {
                Ok(task_list) => {
                    for item in task_list {
                        match item.task_type {
                            1 => {
                                delay.insert_at(
                                    TaskRepr::AssignUser(item.context.parse::<i32>().unwrap()),
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
