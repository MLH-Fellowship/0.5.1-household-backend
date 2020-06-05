table! {
    house (id) {
        id -> Int4,
        name -> Text,
        description -> Text,
    }
}

table! {
    task (id) {
        id -> Int4,
        name -> Text,
        house_id -> Int4,
        description -> Text,
        frequency -> Int4,
    }
}

table! {
    user (id) {
        id -> Int4,
        username -> Text,
        email -> Text,
        password_hash -> Text,
    }
}

table! {
    user_houses (user_id, house_id) {
        user_id -> Int4,
        house_id -> Int4,
    }
}

table! {
    user_task (id) {
        id -> Int4,
        user_id -> Int4,
        task_id -> Int4,
        deadline -> Int4,
        done -> Bool,
    }
}

table! {
    worker_task (id) {
        id -> Int4,
        complete_at -> Timestamp,
        task_type -> Int4,
        context -> Text,
    }
}

joinable!(task -> house (house_id));
joinable!(user_houses -> house (house_id));
joinable!(user_houses -> user (user_id));
joinable!(user_task -> task (task_id));
joinable!(user_task -> user (user_id));

allow_tables_to_appear_in_same_query!(
    house,
    task,
    user,
    user_houses,
    user_task,
    worker_task,
);
