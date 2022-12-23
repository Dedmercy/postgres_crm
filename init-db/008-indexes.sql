-- indexes
CREATE INDEX account_account_id_indx ON account(account_id);
CREATE INDEX account_login_indx ON account(login);
CREATE INDEX editing_indx ON editing(task_id, editing_num);
CREATE INDEX perk_indx ON perk(perk_id);
CREATE INDEX review_account_id_indx ON review(account_id);
CREATE INDEX review_account_review_num_indx ON review(account_id, review_num);
CREATE INDEX service_account_id_indx ON service(account_id);
CREATE INDEX service_perk_id_account_id_indx ON service(perk_id, account_id);
CREATE INDEX specialization_indx ON specialization(sp_id);
CREATE INDEX task_indx ON task(task_id);
CREATE INDEX task_status_indx ON task_status(task_id);
CREATE INDEX user_personal_data_indx ON user_personal_data(user_data_id);


