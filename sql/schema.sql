-- TalentSprint Dashboard — Supabase Schema
-- Run this in the Supabase SQL Editor before first use.

create extension if not exists "pgcrypto";

create table if not exists programs (
  id            uuid primary key default gen_random_uuid(),
  short_name    text not null unique,
  full_name     text not null,
  cohort        int,
  display_order int not null default 99,
  active        boolean not null default true,
  created_at    timestamptz not null default now()
);

create table if not exists sessions (
  id               uuid primary key default gen_random_uuid(),
  program_id       uuid not null references programs(id) on delete cascade,
  topic            text,
  session_date     date not null,
  session_time     text,
  instructor       text,
  batch_strength   int,
  zoom_joined      int,
  total_responses  int,
  avg_rating       numeric(4,2),
  created_at       timestamptz not null default now(),
  unique (program_id, session_date, topic)
);

create table if not exists responses (
  id                uuid primary key default gen_random_uuid(),
  session_id        uuid not null references sessions(id) on delete cascade,
  respondent_name   text,
  respondent_email  text,
  rating            int check (rating between 1 and 10),
  reason            text,
  remarks           text
);
