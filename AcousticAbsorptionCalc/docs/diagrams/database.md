###  dbdiagram.io
URL: https://dbdiagram.io/d

```
Table materials {
  pkey integer [pk]
  type varchar(100)
  name varchar(100)
  _120 numeric(22,2)
  _250 numeric(22,2)
  _500 numeric(22,2)
  _1000 numeric(22,2)
  _2000 numeric(22,2)
  _4000 numeric(22,2)
}

Table norms {
  pkey integer [pk]
  name text
}

Table norms_absorption_multiplayer {
  norm_id integer [ref: > norms.pkey]
  absorption_multiplayer numeric(22,2)
}



Table users {
  id integer [pk, increment]
  username varchar
  email varchar [unique]
  password_hash varchar
  role varchar
  created_at timestamp
}

Table projects {
  id integer [pk, increment]
  user_id integer [ref: > users.id]
  name varchar
  description text
  created_at timestamp
}

Table rooms {
  id integer [pk, increment]
  project_id integer [ref: > projects.id]
  name varchar
  width numeric
  length numeric
  height numeric
  created_at timestamp
}

Table room_materials {
  id integer [pk, increment]
  room_id integer [ref: > rooms.id]
  material_id integer [ref: > materials.pkey]
  location varchar
}

Table furnishings {
  id integer [pk, increment]
  room_id integer [ref: > rooms.id]
  name varchar
  material_id integer [ref: > materials.pkey]
  quantity integer
}

Table calculations {
  id integer [pk, increment]
  room_id integer [ref: > rooms.id]
  reverberation_time numeric
  norm_id integer [ref: > norms.pkey]
  is_within_norm boolean
  created_at timestamp
}

Table project_notes {
  id integer [pk, increment]
  project_id integer [ref: > projects.id]
  room_id integer [ref: > rooms.id, null]
  content text
  created_at timestamp
}

Table shared_projects {
  id integer [pk, increment]
  project_id integer [ref: > projects.id]
  shared_with_user_id integer [ref: > users.id]
  access_level varchar
}

Table change_logs {
  id integer [pk, increment]
  entity_type varchar
  entity_id integer
  changed_by integer [ref: > users.id]
  change_type varchar
  timestamp timestamp
}
```