-- create extension pg_trgm;
-- createdb -O dba -E UTF8 va3

create table word_banks(id integer primary key, name varchar(50));
create table bank_word(wb_id integer, idx integer, wd_id integer, m_indice varchar(50), primary key(wb_id, idx));
create table word_defs(id integer primary key, word varchar(50));
create index on word_defs(word);
create index on word_defs using gin (word gin_trgm_ops);
create table word_meanings(wd_id integer, idx integer, p_of_s varchar(10), meaning varchar(50), primary key(wd_id, idx));
create table verb_forms(wd_id integer primary key, past_form varchar(50), pp_form varchar(50), ing_form varchar(50));

insert into word_banks values(0, 'two-goats-level-2');
insert into bank_word values(0, 0, 0, '0');
insert into bank_word values(0, 1, 1, '0');
insert into bank_word values(0, 2, 2, '0,1');
insert into bank_word values(0, 3, 3, '0');
insert into bank_word values(0, 4, 4, '0');
insert into bank_word values(0, 5, 5, '0');
insert into bank_word values(0, 6, 6, '0');
insert into bank_word values(0, 7, 7, '0');
insert into bank_word values(0, 8, 8, '0');
insert into bank_word values(0, 9, 9, '0');
insert into bank_word values(0, 10, 10, '0');
insert into bank_word values(0, 11, 11, '0');
insert into bank_word values(0, 12, 19, '0');

insert into word_banks values(1, 'fighting-goats-and-jackal-level-2');
insert into bank_word values(1, 0, 12, '0');
insert into bank_word values(1, 1, 13, '0');
insert into bank_word values(1, 2, 14, '0');
insert into bank_word values(1, 3, 15, '0');
insert into bank_word values(1, 4, 16, '0');
insert into bank_word values(1, 5, 17, '0');
insert into bank_word values(1, 6, 18, '0,1');


create sequence word_def_seq;
select setval('word_def_seq', 20);

create sequence word_bank_seq;
select setval('word_bank_seq', 10);

create sequence practice_seq;
select setval('practice_seq', 10);

create sequence sentence_seq;
select setval('sentence_seq', 10);

insert into word_defs values(0, 'steep');
insert into word_meanings values(0, 0, 'adj', '陡峭（斜）的');
insert into word_defs values(1, 'mountain');
insert into word_meanings values(1, 0, 'n', '山');
insert into word_defs values(2, 'flow');
insert into word_meanings values(2, 0, 'v', '流動');
insert into word_meanings values(2, 1, 'n', '流');
insert into word_defs values(3, 'trunk');
insert into word_meanings values(3, 0, 'n', '樹幹');
insert into word_meanings values(3, 1, 'n', '象鼻');
insert into word_meanings values(3, 2, 'n', '大木箱');
insert into word_defs values(4, 'squirrel');
insert into word_meanings values(4, 0, 'n', '松鼠');
insert into word_defs values(5, 'valley');
insert into word_meanings values(5, 0, 'n', '山谷');
insert into word_defs values(6, 'rock');
insert into word_meanings values(6, 0, 'n', '岩石');
insert into word_defs values(7, 'scared');
insert into word_meanings values(7, 0, 'adj', '害怕的');
insert into word_defs values(8, 'opposite');
insert into word_meanings values(8, 0, 'adj', '相反的');
insert into word_defs values(9, 'direction');
insert into word_meanings values(9, 0, 'n', '方向');
insert into word_defs values(10, 'horn');
insert into word_meanings values(10, 0, 'n', '（動物）角');
insert into word_meanings values(10, 1, 'n', '號角');
insert into word_defs values(11, 'gap');
insert into word_meanings values(11, 0, 'n', '空隙');
insert into word_defs values(12, 'wise');
insert into word_meanings values(12, 0, 'adj', '明智的');
insert into word_defs values(13, 'jackal');
insert into word_meanings values(13, 0, 'n', '豺');
insert into word_defs values(14, 'greedy');
insert into word_meanings values(14, 0, 'adj', '貪心的');
insert into word_defs values(15, 'blood');
insert into word_meanings values(15, 0, 'n', '血');
insert into word_defs values(16, 'goat');
insert into word_meanings values(16, 0, 'n', '山羊');
insert into word_defs values(17, 'injure');
insert into word_meanings values(17, 0, 'v', '使受傷');
insert into word_defs values(18, 'fight');
insert into word_meanings values(18, 0, 'n', '打鬥');
insert into word_meanings values(18, 1, 'v', '打鬥');
insert into verb_forms values(18, 'fought', 'fought', NULL);
insert into word_defs values(19, 'river');
insert into word_meanings values(19, 0, 'n', '河流');


create sequence exercise_seq;
select setval('exercise_seq', 10);

create table practices(id integer primary key, wb_id integer, fr_idx integer, to_idx integer, hard_only boolean, assess_dt date, stu_id integer);
create table practice_hard(p_id integer, w_idx integer, primary key(p_id, w_idx));
create table sprints(id integer primary key, start_dt date, stu_id integer);
create index on sprints(stu_id);
create table sprint_practice(sp_id integer, p_id integer, primary key(sp_id, p_id));
create table exercises(id integer primary key, dt date);
create table exercise_word(e_id integer, wd_id integer, m_indice varchar(50), primary key(e_id, wd_id));
create table exercise_snt(e_id integer, s_id integer, primary key(e_id, s_id));
create table sprint_exercise(sp_id integer, e_id integer, primary key(sp_id, e_id));

insert into practices values(0, 0, 0, 10, 'f', '2023-12-1', 0);
insert into practice_hard values(0, 1);
insert into practice_hard values(0, 3);
insert into practice_hard values(0, 8);
insert into practices values(1, 1, 0, 6, 'f', '2023-12-2', 0);
insert into sprints values(0, '2023-12-4', 0);
insert into sprint_practice values(0, 0);
insert into sprint_practice values(0, 1);
insert into exercises values(0, '2023-12-4');
insert into exercises values(1, '2023-12-5');
insert into sprint_exercise values(0, 0);
insert into sprint_exercise values(0, 1);
insert into exercise_word values(0, 0, '0');
insert into exercise_word values(0, 1, '0');
insert into exercise_word values(0, 2, '0');
insert into exercise_word values(0, 3, '0');
insert into exercise_word values(0, 11, '0');
insert into exercise_word values(0, 13, '0');
insert into exercise_word values(0, 14, '0');
insert into exercise_word values(0, 17, '0');
insert into exercise_word values(1, 0, '0');
insert into exercise_word values(1, 2, '0');
insert into exercise_word values(1, 4, '0');
insert into exercise_word values(1, 5, '0');
insert into exercise_word values(1, 10, '0');
insert into exercise_word values(1, 11, '0');
insert into exercise_snt values(0, 0);
insert into exercise_snt values(0, 1);
insert into exercise_snt values(0, 2);
insert into exercise_snt values(1, 3);
insert into exercise_snt values(1, 4);
insert into exercise_snt values(1, 5);


create table sentences(id integer primary key, text varchar(100));
create index on sentences(text);
create table snt_keywords(snt_id integer, wd_id integer, wm_idx integer, primary key(snt_id, wd_id, wm_idx));
create index on snt_keywords(wd_id);

insert into sentences values(0, '這個山很陡峭。');
insert into snt_keywords values(0, 1, 0);
insert into snt_keywords values(0, 0, 0);
insert into sentences values(1, '這條河裡的水在快速地流動。');
insert into snt_keywords values(1, 19, 0);
insert into snt_keywords values(1, 2, 0);
insert into sentences values(2, '一隻松鼠爬上了這條樹幹。');
insert into snt_keywords values(2, 4, 0);
insert into snt_keywords values(2, 3, 0);
insert into sentences values(3, '一隻松鼠住在這個山谷裡。');
insert into snt_keywords values(3, 4, 0);
insert into snt_keywords values(3, 5, 0);
insert into sentences values(4, '這個山上的岩石很堅硬。');
insert into snt_keywords values(4, 6, 0);
insert into snt_keywords values(4, 1, 0);
insert into sentences values(5, '這個山谷裡的空氣慢慢地流動。');
insert into snt_keywords values(5, 2, 0);
insert into snt_keywords values(5, 5, 0);
insert into sentences values(6, '那隻害怕的松鼠去了相反的方向。');
insert into snt_keywords values(6, 4, 0);
insert into snt_keywords values(6, 7, 0);
insert into snt_keywords values(6, 8, 0);
insert into snt_keywords values(6, 9, 0);

create sequence student_seq;
select setval('student_seq', 10);

create sequence teacher_seq;
select setval('teacher_seq', 10);

create table students(id integer primary key, name varchar(100), t_id integer);
create index on students(name);
create index on students using gin (name gin_trgm_ops);
create index on students(t_id);
insert into students values(0, 'Jodie', 0);
insert into students values(1, 'Holly', 0);

create table teachers(id integer primary key, gmail varchar(100));
insert into teachers values(0, 'kent.tong.mo@gmail.com');
create index on teachers(gmail);