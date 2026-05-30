START TRANSACTION;
USE `garage_erp`;

-- -----------------------------------------------------
-- Init t_schedule_type
-- -----------------------------------------------------
INSERT INTO `garage_erp`.`t_schedule_type` (`id`, `name`)
VALUES (1, 'annual leave');


-- -----------------------------------------------------
-- Init t_schedule_type
-- -----------------------------------------------------
INSERT INTO `garage_erp`.`t_role` (`id`, `title`)
VALUES (1, 'garage owner');


-- -----------------------------------------------------
-- Init t_job_card_status
-- -----------------------------------------------------
INSERT INTO `garage_erp`.`t_job_card_status_type` (`id`, `status`)
VALUES (1, 'closed'),
       (2, 'pending'),
       (3, 'ongoing'),
       (4, 'ready for pick up');


-- -----------------------------------------------------
-- Init t_job_card_pending_status_type
-- -----------------------------------------------------
INSERT INTO `garage_erp`.`t_job_card_pending_status_type` (`id`, `status`)
VALUES (1, 'Pending - Waiting Technicians'),
       (2, 'Pending - Waiting Parts');


-- -----------------------------------------------------
-- Init t_job_card_unfinished_status_type
-- -----------------------------------------------------
INSERT INTO `garage_erp`.`t_job_card_unfinished_status_type` (`id`, `status`)
VALUES (1, 'Payment pending'),
       (2, 'Payment done');


COMMIT;