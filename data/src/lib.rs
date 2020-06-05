#[macro_use]
extern crate diesel;

pub mod schema;

use schema::{house, task, user_task};

#[derive(Queryable)]
pub struct User {
    pub id: i32,
    pub username: String,
    pub email: String,
    pub email_verified: bool,
    pub password_hash: String,
}

#[derive(Queryable, Identifiable)]
#[table_name = "task"]
pub struct Task {
    pub id: i32,
    pub name: String,
    pub house_id: i32,
    pub description: String,
    pub frequency: i32,
}

#[derive(Queryable, Identifiable)]
#[table_name = "house"]
pub struct House {
    pub id: i32,
    pub name: String,
    pub description: String,
}

#[derive(Queryable)]
pub struct UserTask {
    pub id: i32,
    pub task_id: i32,
    pub user_id: i32,
    pub deadline: i32,
    pub done: bool,
}

#[derive(Insertable)]
#[table_name = "user_task"]
pub struct NewUserTask {
    pub task_id: i32,
    pub user_id: i32,
    pub deadline: i32,
    pub done: bool,
}
#[derive(Queryable)]
struct UserHouse {
    pub house_id: i32,
    pub user_id: i32,
}

#[derive(Queryable)]
pub struct WorkerTask {
    pub id: i32,
    pub complete_at: chrono::NaiveDateTime,
    pub task_type: i32,
    pub context: String,
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
