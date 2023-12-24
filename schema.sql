-- create database va3 character set UTF8;
-- grant all on va3.* to 'dba'@'localhost';

-- create database va3_test character set UTF8;
-- grant all on va3_test.* to 'dba'@'localhost';

-- mysqldump -u root -p va3 > va3.dump
-- mysql -u root -p < va3.dump

create table word_defs(id integer auto_increment primary key, word varchar(50));
create index word_defs_idx_word on word_defs(word);
create table word_meanings(wd_id integer, idx integer, p_of_s varchar(10), 
                          meaning varchar(50), 
                          form1 varchar(50), form2 varchar(50), form3 varchar(50), 
                          primary key(wd_id, idx));

create table word_banks(id integer auto_increment primary key, name varchar(50));
create table bank_word(wb_id integer, idx integer, wd_id integer, m_indice varchar(50), primary key(wb_id, idx));

create table practices(id integer auto_increment primary key, wb_id integer, fr_idx integer, to_idx integer, hard_only boolean, assess_dt date, stu_id integer);
create table practice_hard(p_id integer, w_idx integer, primary key(p_id, w_idx));
create table sprints(id integer auto_increment primary key, start_dt date, stu_id integer);
create index sprints_idx_stu_id on sprints(stu_id);
create table sprint_practice(sp_id integer, p_id integer, primary key(sp_id, p_id));
create table exercises(id integer auto_increment primary key, dt date);
create table exercise_word(e_id integer, wd_id integer, m_indice varchar(50), primary key(e_id, wd_id));
create table exercise_snt(e_id integer, s_id integer, primary key(e_id, s_id));
create table sprint_exercise(sp_id integer, e_id integer, primary key(sp_id, e_id));

create table sentences(id integer auto_increment primary key, text varchar(100));
create index sentences_idx_text on sentences(text);
create table snt_keywords(snt_id integer, wd_id integer, wm_idx integer, primary key(snt_id, wd_id, wm_idx));
create index snt_keywords_idx_wd_id on snt_keywords(wd_id);

create table students(id integer auto_increment primary key, name varchar(100));
create index students_idx_name on students(name);
create table teachers(id integer auto_increment primary key, gmail varchar(100));
create index teachers_idx_email on teachers(gmail);
create table teacher_student(tch_id integer, stu_id integer, primary key(tch_id, stu_id));

insert into students values(1, 'Jodie');
insert into students values(2, 'Holly');

insert into teachers values(1, 'kent.tong.mo@gmail.com');

insert into teacher_student values(1, 1);
insert into teacher_student values(1, 2);


insert into word_defs values(1, 'steep');
insert into word_meanings values(1, 0, 'adj', '陡峭（斜）的', NULL, NULL, NULL);
insert into word_defs values(2, 'mountain');
insert into word_meanings values(2, 0, 'n', '山', NULL, NULL, NULL);
insert into word_defs values(3, 'flow');
insert into word_meanings values(3, 0, 'v', '流動', NULL, NULL, NULL);
insert into word_meanings values(3, 1, 'n', '流', NULL, NULL, NULL);
insert into word_defs values(4, 'trunk');
insert into word_meanings values(4, 0, 'n', '樹幹', NULL, NULL, NULL);
insert into word_meanings values(4, 1, 'n', '象鼻', NULL, NULL, NULL);
insert into word_meanings values(4, 2, 'n', '大木箱', NULL, NULL, NULL);
insert into word_defs values(5, 'squirrel');
insert into word_meanings values(5, 0, 'n', '松鼠', NULL, NULL, NULL);
insert into word_defs values(6, 'valley');
insert into word_meanings values(6, 0, 'n', '山谷', NULL, NULL, NULL);
insert into word_defs values(7, 'rock');
insert into word_meanings values(7, 0, 'n', '岩石', NULL, NULL, NULL);
insert into word_defs values(8, 'scared');
insert into word_meanings values(8, 0, 'adj', '害怕的', NULL, NULL, NULL);
insert into word_defs values(9, 'opposite');
insert into word_meanings values(9, 0, 'adj', '相反的', NULL, NULL, NULL);
insert into word_defs values(10, 'direction');
insert into word_meanings values(10, 0, 'n', '方向', NULL, NULL, NULL);
insert into word_defs values(11, 'horn');
insert into word_meanings values(11, 0, 'n', '（動物）角', NULL, NULL, NULL);
insert into word_meanings values(11, 1, 'n', '號角', NULL, NULL, NULL);
insert into word_defs values(12, 'gap');
insert into word_meanings values(12, 0, 'n', '空隙', NULL, NULL, NULL);
insert into word_defs values(13, 'wise');
insert into word_meanings values(13, 0, 'adj', '明智的', NULL, NULL, NULL);
insert into word_defs values(14, 'jackal');
insert into word_meanings values(14, 0, 'n', '豺', NULL, NULL, NULL);
insert into word_defs values(15, 'greedy');
insert into word_meanings values(15, 0, 'adj', '貪心的', NULL, NULL, NULL);
insert into word_defs values(16, 'blood');
insert into word_meanings values(16, 0, 'n', '血', NULL, NULL, NULL);
insert into word_defs values(17, 'goat');
insert into word_meanings values(17, 0, 'n', '山羊', NULL, NULL, NULL);
insert into word_defs values(18, 'injure');
insert into word_meanings values(18, 0, 'v', '使受傷', NULL, NULL, NULL);
insert into word_meanings values(18, 1, 'v', '損毀', NULL, NULL, NULL);
insert into word_defs values(19, 'fight');
insert into word_meanings values(19, 0, 'n', '打鬥', NULL, NULL, NULL);
insert into word_meanings values(19, 1, 'v', '打鬥', 'fought', 'fought', NULL);
insert into word_defs values(20, 'river');
insert into word_meanings values(20, 0, 'n', '河流', NULL, NULL, NULL);
insert into word_defs values(21, 'person');
insert into word_meanings values(21, 0, 'n', '人', 'people', NULL, NULL);

insert into word_banks values(1, 'two-goats-level-2');
insert into bank_word values(1, 0, 1, '0');
insert into bank_word values(1, 1, 2, '0');
insert into bank_word values(1, 2, 3, '0,1');
insert into bank_word values(1, 3, 4, '0');
insert into bank_word values(1, 4, 5, '0');
insert into bank_word values(1, 5, 6, '0');
insert into bank_word values(1, 6, 7, '0');
insert into bank_word values(1, 7, 8, '0');
insert into bank_word values(1, 8, 9, '0');
insert into bank_word values(1, 9, 10, '0');
insert into bank_word values(1, 10, 11, '0');
insert into bank_word values(1, 11, 12, '0');
insert into bank_word values(1, 12, 20, '0');

insert into word_banks values(2, 'fighting-goats-and-jackal-level-2');
insert into bank_word values(2, 0, 12, '0');
insert into bank_word values(2, 1, 13, '0');
insert into bank_word values(2, 2, 14, '0');
insert into bank_word values(2, 3, 15, '0');
insert into bank_word values(2, 4, 16, '0');
insert into bank_word values(2, 5, 17, '0');
insert into bank_word values(2, 6, 18, '0,1');

insert into word_banks values(3, 'wb-A');
insert into bank_word values(3, 0, 19, '0,1F');
insert into bank_word values(3, 1, 21, '0F');

insert into practices values(1, 1, 0, 10, false, '2023-12-1', 1);
insert into practice_hard values(1, 1);
insert into practice_hard values(1, 3);
insert into practice_hard values(1, 8);
insert into practices values(2, 2, 0, 6, false, '2023-12-2', 1);
insert into practices values(3, 1, 4, 9, true, '2023-12-4', 2);
insert into practice_hard values(3, 5);
insert into practice_hard values(3, 6);

insert into sprints values(1, '2023-12-4', 1);
insert into sprint_practice values(1, 1);
insert into sprint_practice values(1, 2);
insert into exercises values(1, '2023-12-4');
insert into exercises values(2, '2023-12-5');
insert into sprint_exercise values(1, 1);
insert into sprint_exercise values(1, 2);
insert into exercise_word values(1, 1, '0');
insert into exercise_word values(1, 2, '0');
insert into exercise_word values(1, 3, '0');
insert into exercise_word values(1, 4, '0');
insert into exercise_word values(1, 12, '0');
insert into exercise_word values(1, 14, '0');
insert into exercise_word values(1, 15, '0');
insert into exercise_word values(1, 18, '0');
insert into exercise_word values(2, 1, '0');
insert into exercise_word values(2, 3, '0');
insert into exercise_word values(2, 5, '0');
insert into exercise_word values(2, 6, '0');
insert into exercise_word values(2, 11, '0');
insert into exercise_word values(2, 12, '0');
insert into exercise_snt values(1, 1);
insert into exercise_snt values(1, 2);
insert into exercise_snt values(1, 3);
insert into exercise_snt values(2, 4);
insert into exercise_snt values(2, 5);
insert into exercise_snt values(2, 6);


insert into sentences values(1, '這個山很陡峭。');
insert into snt_keywords values(1, 2, 0);
insert into snt_keywords values(1, 1, 0);
insert into sentences values(2, '這條河裡的水在快速地流動。');
insert into snt_keywords values(2, 20, 0);
insert into snt_keywords values(2, 3, 0);
insert into sentences values(3, '一隻松鼠爬上了這條樹幹。');
insert into snt_keywords values(3, 5, 0);
insert into snt_keywords values(3, 4, 0);
insert into sentences values(4, '一隻松鼠住在這個山谷裡。');
insert into snt_keywords values(4, 5, 0);
insert into snt_keywords values(4, 6, 0);
insert into sentences values(5, '這個山上的岩石很堅硬。');
insert into snt_keywords values(5, 7, 0);
insert into snt_keywords values(5, 2, 0);
insert into sentences values(6, '這個山谷裡的空氣慢慢地流動。');
insert into snt_keywords values(6, 3, 0);
insert into snt_keywords values(6, 6, 0);
insert into sentences values(7, '那隻害怕的松鼠去了相反的方向。');
insert into snt_keywords values(7, 5, 0);
insert into snt_keywords values(7, 8, 0);
insert into snt_keywords values(7, 9, 0);
insert into snt_keywords values(7, 10, 0);

