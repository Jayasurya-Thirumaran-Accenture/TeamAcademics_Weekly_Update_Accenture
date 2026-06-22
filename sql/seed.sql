-- TalentSprint Dashboard — Seed Data
-- Run AFTER schema.sql to populate the initial 4 programs.

insert into programs (short_name, full_name, cohort, display_order) values
  ('ADSML C9',       'PG Level Advanced Programme in Applied Data Science and Machine Learning', 9,  1),
  ('TS GenAI C2',    'TalentSprint Generative AI Programme',                                    2,  2),
  ('IIITH GIAPT C1', 'IIIT Hyderabad Global Initiative in AI and Programme Technology',         1,  3),
  ('AIML C27',       'Artificial Intelligence and Machine Learning Programme',                  27, 4)
on conflict (short_name) do nothing;
