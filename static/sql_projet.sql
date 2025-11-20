
DROP TABLE IF EXISTS Asso_15;
DROP TABLE IF EXISTS Asso_14;
DROP TABLE IF EXISTS Asso_10;
DROP TABLE IF EXISTS Asso_9;
DROP TABLE IF EXISTS Asso_8;
DROP TABLE IF EXISTS RECUPERE;
DROP TABLE IF EXISTS ASSOCIE_A_;
DROP TABLE IF EXISTS DISTANCE_ENTRE;
DROP TABLE IF EXISTS ACHAT_VETEMENT;
DROP TABLE IF EXISTS COLLECTE_VETEMENT;
DROP TABLE IF EXISTS DEPOSE;
DROP TABLE IF EXISTS ACHAT;
DROP TABLE IF EXISTS DEPOT;
DROP TABLE IF EXISTS CAMIONETTE;
DROP TABLE IF EXISTS COLLECTE;
DROP TABLE IF EXISTS BENNE;
DROP TABLE IF EXISTS CATEGORIE_VETEMENTS;
DROP TABLE IF EXISTS CLIENT;


CREATE TABLE CLIENT(
   id_client VARCHAR(50),
   nom VARCHAR(50),
   prénom VARCHAR(50),
   adresse VARCHAR(50),
   téléphone VARCHAR(50),
   email VARCHAR(50),
   total_kg_achetés VARCHAR(50),
   date_1ere_achat VARCHAR(50),
   point_fidelite VARCHAR(50),
   PRIMARY KEY(id_client)
);

CREATE TABLE CATEGORIE_VETEMENTS(
   id_categorie_vetement VARCHAR(50),
   nom_vetement VARCHAR(50),
   prix_kg VARCHAR(50),
   PRIMARY KEY(id_categorie_vetement)
);

CREATE TABLE BENNE(
   id_benne VARCHAR(50),
   adresse_benne VARCHAR(50),
   distance_magasin VARCHAR(50),
   coordonnees_gps VARCHAR(50),
   PRIMARY KEY(id_benne)
);

CREATE TABLE COLLECTE(
   id_collecte VARCHAR(50),
   date_collecte DATE,
   duree_collecte VARCHAR(50),
   PRIMARY KEY(id_collecte)
);

CREATE TABLE CAMIONETTE(
   id_camionette VARCHAR(50),
   immatriculation VARCHAR(50),
   capacite_max VARCHAR(50),
   PRIMARY KEY(id_camionette)
);

CREATE TABLE ACHAT(
   id_achat INT,
   montant_total VARCHAR(50) NOT NULL,
   date_achat DATE,
   poids_total VARCHAR(50),
   client_id VARCHAR(50),
   PRIMARY KEY(id_achat),
   FOREIGN KEY(client_id) REFERENCES CLIENT(id_client)
);

CREATE TABLE DEPOT(
   id_depot VARCHAR(50),
   PRIMARY KEY(id_depot)
);

CREATE TABLE DEPOSE(
   num_depot INT,
   date_depot DATE,
   PRIMARY KEY(num_depot)
);

CREATE TABLE COLLECTE_VETEMENT(
   id_collecte_vetement VARCHAR(50),
   date_collecte DATE,
   quantite_vetement VARCHAR(50),
   collecte_id VARCHAR(50) NOT NULL,
   categorie_vetement_id VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_collecte_vetement),
   FOREIGN KEY(collecte_id) REFERENCES COLLECTE(id_collecte),
   FOREIGN KEY(categorie_vetement_id) REFERENCES CATEGORIE_VETEMENTS(id_categorie_vetement)
);

CREATE TABLE ACHAT_VETEMENT(
   id_achat_vetement VARCHAR(50),
   quantite_achete VARCHAR(50),
   PRIMARY KEY(id_achat_vetement)
);

CREATE TABLE DISTANCE_ENTRE(
   id_benne VARCHAR(50),
   id_benne_1 VARCHAR(50),
   distance_inter_benne VARCHAR(50),
   PRIMARY KEY(id_benne, id_benne_1),
   FOREIGN KEY(id_benne) REFERENCES BENNE(id_benne),
   FOREIGN KEY(id_benne_1) REFERENCES BENNE(id_benne)
);

CREATE TABLE ASSOCIE_A_(
   id_collecte VARCHAR(50),
   id_camionette VARCHAR(50),
   PRIMARY KEY(id_collecte, id_camionette),
   FOREIGN KEY(id_collecte) REFERENCES COLLECTE(id_collecte),
   FOREIGN KEY(id_camionette) REFERENCES CAMIONETTE(id_camionette)
);

CREATE TABLE RECUPERE(
   id_benne VARCHAR(50),
   id_collecte VARCHAR(50),
   PRIMARY KEY(id_benne, id_collecte),
   FOREIGN KEY(id_benne) REFERENCES BENNE(id_benne),
   FOREIGN KEY(id_collecte) REFERENCES COLLECTE(id_collecte)
);

CREATE TABLE Asso_8(
   id_client VARCHAR(50),
   num_depot INT,
   PRIMARY KEY(id_client, num_depot),
   FOREIGN KEY(id_client) REFERENCES CLIENT(id_client),
   FOREIGN KEY(num_depot) REFERENCES DEPOSE(num_depot)
);

CREATE TABLE Asso_9(
   id_categorie_vetement VARCHAR(50),
   num_depot INT,
   PRIMARY KEY(id_categorie_vetement, num_depot),
   FOREIGN KEY(id_categorie_vetement) REFERENCES CATEGORIE_VETEMENTS(id_categorie_vetement),
   FOREIGN KEY(num_depot) REFERENCES DEPOSE(num_depot)
);

CREATE TABLE Asso_10(
   id_depot VARCHAR(50),
   num_depot INT,
   PRIMARY KEY(id_depot, num_depot),
   FOREIGN KEY(id_depot) REFERENCES DEPOT(id_depot),
   FOREIGN KEY(num_depot) REFERENCES DEPOSE(num_depot)
);

CREATE TABLE Asso_14(
   id_categorie_vetement VARCHAR(50),
   id_achat_vetement VARCHAR(50),
   PRIMARY KEY(id_categorie_vetement, id_achat_vetement),
   FOREIGN KEY(id_categorie_vetement) REFERENCES CATEGORIE_VETEMENTS(id_categorie_vetement),
   FOREIGN KEY(id_achat_vetement) REFERENCES ACHAT_VETEMENT(id_achat_vetement)
);

CREATE TABLE Asso_15(
   id_achat INT,
   id_achat_vetement VARCHAR(50),
   PRIMARY KEY(id_achat, id_achat_vetement),
   FOREIGN KEY(id_achat) REFERENCES ACHAT(id_achat),
   FOREIGN KEY(id_achat_vetement) REFERENCES ACHAT_VETEMENT(id_achat_vetement)
);

INSERT INTO CATEGORIE_VETEMENTS VALUES
('CAT001','T-shirt','8.50'),('CAT002','Pantalon','12.00'),('CAT003','Robe','15.00'),
('CAT004','Pull','11.00'),('CAT005','Veste','18.00'),('CAT006','Jean','14.00'),
('CAT007','Short','7.50'),('CAT008','Chemise','10.50'),('CAT009','Manteau','22.00'),
('CAT010','Vêtement Enfant','6.00');


INSERT INTO CLIENT VALUES
('CLI001','Martin','Sophie','12 rue Pasteur','0612345678','sophie.martin@email.fr','45.5','2023-01-15','455'),
('CLI002','Dubois','Pierre','8 av Victor Hugo','0623456789','pierre.dubois@email.fr','32.0','2023-02-20','320'),
('CLI003','Bernard','Marie','45 bd Carnot','0634567890','marie.bernard@email.fr','67.8','2023-01-10','678'),
('CLI004','Petit','Jean','3 pl Mairie','0645678901','jean.petit@email.fr','28.5','2023-03-05','285'),
('CLI005','Robert','Claire','19 rue Paix','0656789012','claire.robert@email.fr','54.2','2023-02-12','542'),
('CLI006','Richard','Luc','7 imp Fleurs','0667890123','luc.richard@email.fr','41.0','2023-04-18','410'),
('CLI007','Durand','Emma','25 av Foch','0678901234','emma.durand@email.fr','89.3','2023-01-22','893'),
('CLI008','Moreau','Thomas','14 rue Gambetta','0689012345','thomas.moreau@email.fr','36.7','2023-03-30','367'),
('CLI009','Simon','Julie','9 cours Lafayette','0690123456','julie.simon@email.fr','72.5','2023-02-08','725'),
('CLI010','Laurent','Nicolas','31 rue Commerce','0601234567','nicolas.laurent@email.fr','25.8','2023-05-14','258'),
('CLI011','Lefebvre','Camille','18 av Jaurès','0612345679','camille.lefebvre@email.fr','58.9','2023-01-28','589'),
('CLI012','Michel','Antoine','6 pl Wilson','0623456780','antoine.michel@email.fr','43.2','2023-04-05','432'),
('CLI013','Garcia','Léa','22 rue Verdun','0634567891','lea.garcia@email.fr','91.4','2023-01-19','914'),
('CLI014','David','Marc','11 bd Diderot','0645678902','marc.david@email.fr','34.6','2023-03-22','346'),
('CLI015','Bertrand','Sarah','5 imp Moulin','0656789013','sarah.bertrand@email.fr','62.1','2023-02-15','621'),
('CLI016','Roux','Alexandre','29 av Gare','0667890124','alexandre.roux@email.fr','48.7','2023-04-28','487'),
('CLI017','Vincent','Manon','13 rue St-Martin','0678901235','manon.vincent@email.fr','76.3','2023-01-30','763'),
('CLI018','Fournier','Hugo','20 cours Berriat','0689012346','hugo.fournier@email.fr','39.5','2023-03-12','395'),
('CLI019','Girard','Chloé','8 pl République','0690123457','chloe.girard@email.fr','85.2','2023-02-25','852'),
('CLI020','Bonnet','Maxime','16 rue Alsace','0601234568','maxime.bonnet@email.fr','31.9','2023-05-08','319');


INSERT INTO BENNE VALUES
('BEN001','5 rue Gare','2.5','45.1885,5.7245'),
('BEN002','18 av Jaurès','3.2','45.1912,5.7289'),
('BEN003','12 pl Hugo','1.8','45.1867,5.7198'),
('BEN004','25 bd Gambetta','4.1','45.1945,5.7356'),
('BEN005','8 rue Pasteur','2.9','45.1823,5.7134'),
('BEN006','33 cours Berriat','5.3','45.1789,5.7089'),
('BEN007','14 av Alsace','3.7','45.1934,5.7312'),
('BEN008','21 pl Grenette','2.1','45.1901,5.7267');


INSERT INTO DISTANCE_ENTRE VALUES
('BEN001','BEN002','1.2'),('BEN001','BEN003','0.9'),('BEN002','BEN003','1.5'),
('BEN002','BEN004','1.8'),('BEN003','BEN005','2.1'),('BEN004','BEN005','2.7'),
('BEN005','BEN006','1.3'),('BEN006','BEN007','2.4'),('BEN007','BEN008','1.6');


INSERT INTO CAMIONETTE VALUES
('CAM001','AB-123-CD','800'),
('CAM002','EF-456-GH','1000'),
('CAM003','IJ-789-KL','850');


INSERT INTO COLLECTE VALUES
('COL001','2024-01-05','3:30'),('COL002','2024-01-19','4:15'),('COL003','2024-02-02','3:45'),
('COL004','2024-02-16','4:00'),('COL005','2024-03-01','3:20'),('COL006','2024-03-15','4:30'),
('COL007','2024-03-29','3:55'),('COL008','2024-04-12','4:10'),('COL009','2024-04-26','3:40'),
('COL010','2024-05-10','4:20'),('COL011','2024-05-24','3:25'),('COL012','2024-06-07','4:05'),
('COL013','2024-06-21','3:50'),('COL014','2024-07-05','4:25'),('COL015','2024-07-19','3:35');


INSERT INTO ASSOCIE_A_ VALUES
('COL001','CAM001'),('COL002','CAM002'),('COL003','CAM003'),('COL004','CAM001'),('COL005','CAM002'),
('COL006','CAM003'),('COL007','CAM001'),('COL008','CAM002'),('COL009','CAM003'),('COL010','CAM001'),
('COL011','CAM002'),('COL012','CAM003'),('COL013','CAM001'),('COL014','CAM002'),('COL015','CAM003');


INSERT INTO RECUPERE VALUES
('BEN001','COL001'),('BEN002','COL001'),('BEN003','COL002'),('BEN004','COL002'),
('BEN005','COL003'),('BEN006','COL003'),('BEN007','COL004'),('BEN008','COL004'),
('BEN001','COL005'),('BEN003','COL005'),('BEN002','COL006'),('BEN004','COL006'),
('BEN005','COL007'),('BEN007','COL007'),('BEN006','COL008'),('BEN008','COL008');


INSERT INTO COLLECTE_VETEMENT VALUES
('CV001','2024-01-05','25.5','COL001','CAT001'),('CV002','2024-01-05','18.3','COL001','CAT002'),
('CV003','2024-01-05','32.7','COL001','CAT004'),('CV004','2024-01-19','28.9','COL002','CAT003'),
('CV005','2024-01-19','21.5','COL002','CAT005'),('CV006','2024-01-19','36.4','COL002','CAT006'),
('CV007','2024-02-02','24.6','COL003','CAT001'),('CV008','2024-02-02','17.9','COL003','CAT007'),
('CV009','2024-02-02','31.2','COL003','CAT008'),('CV010','2024-02-16','27.3','COL004','CAT002'),
('CV011','2024-02-16','20.1','COL004','CAT009'),('CV012','2024-02-16','35.8','COL004','CAT010'),
('CV013','2024-03-01','26.5','COL005','CAT001'),('CV014','2024-03-01','19.4','COL005','CAT004'),
('CV015','2024-03-01','33.9','COL005','CAT006'),('CV016','2024-03-15','29.7','COL006','CAT003'),
('CV017','2024-03-15','22.8','COL006','CAT005'),('CV018','2024-03-15','37.5','COL006','CAT007'),
('CV019','2024-03-29','25.1','COL007','CAT002'),('CV020','2024-03-29','18.6','COL007','CAT008'),
('CV021','2024-04-12','32.4','COL008','CAT001'),('CV022','2024-04-12','15.9','COL008','CAT009'),
('CV023','2024-04-26','28.2','COL009','CAT003'),('CV024','2024-04-26','21.7','COL009','CAT010'),
('CV025','2024-05-10','36.1','COL010','CAT004'),('CV026','2024-05-10','19.5','COL010','CAT006'),
('CV027','2024-05-24','24.8','COL011','CAT001'),('CV028','2024-05-24','17.3','COL011','CAT005'),
('CV029','2024-06-07','30.9','COL012','CAT002'),('CV030','2024-06-07','14.6','COL012','CAT007'),
('CV031','2024-06-21','27.6','COL013','CAT008'),('CV032','2024-06-21','20.9','COL013','CAT003'),
('CV033','2024-07-05','34.5','COL014','CAT009'),('CV034','2024-07-05','18.1','COL014','CAT001'),
('CV035','2024-07-19','26.3','COL015','CAT010'),('CV036','2024-07-19','19.8','COL015','CAT004'),
('CV037','2024-01-05','22.4','COL001','CAT007'),('CV038','2024-02-02','29.1','COL003','CAT002'),
('CV039','2024-03-29','23.5','COL007','CAT005'),('CV040','2024-05-10','31.8','COL010','CAT008');


INSERT INTO DEPOT VALUES ('DEP001'),('DEP002'),('DEP003'),('DEP004'),('DEP005');


INSERT INTO DEPOSE VALUES
(1,'2024-01-10'),(2,'2024-02-05'),(3,'2024-03-12'),(4,'2024-04-08'),(5,'2024-05-15'),
(6,'2024-06-20'),(7,'2024-07-10'),(8,'2024-08-05'),(9,'2024-09-12'),(10,'2024-10-18');


INSERT INTO Asso_8 VALUES
('CLI001',1),('CLI002',1),('CLI003',2),('CLI004',2),('CLI005',3),
('CLI006',4),('CLI007',5),('CLI008',6),('CLI009',7),('CLI010',8);


INSERT INTO Asso_9 VALUES
('CAT001',1),('CAT002',1),('CAT003',2),('CAT004',3),('CAT005',4),
('CAT006',5),('CAT007',6),('CAT008',7),('CAT009',8),('CAT010',9);


INSERT INTO Asso_10 VALUES
('DEP001',1),('DEP001',2),('DEP002',3),('DEP002',4),('DEP003',5),
('DEP003',6),('DEP004',7),('DEP004',8),('DEP005',9),('DEP005',10);


INSERT INTO ACHAT VALUES
(1,'135.50','2024-01-20','15.9','CLI001'),(2,'98.00','2024-01-25','8.2','CLI002'),
(3,'210.75','2024-02-03','14.1','CLI003'),(4,'76.50','2024-02-10','6.4','CLI004'),
(5,'165.00','2024-02-18','11.0','CLI005'),(6,'142.80','2024-03-05','11.9','CLI006'),
(7,'255.00','2024-03-12','17.0','CLI007'),(8,'89.25','2024-03-20','7.5','CLI008'),
(9,'198.90','2024-04-02','13.3','CLI009'),(10,'67.50','2024-04-15','5.6','CLI010'),
(11,'178.50','2024-04-22','11.9','CLI011'),(12,'125.40','2024-05-08','10.5','CLI012'),
(13,'298.75','2024-05-15','19.9','CLI013'),(14,'82.00','2024-05-28','6.9','CLI014'),
(15,'187.50','2024-06-05','12.5','CLI015'),(16,'156.00','2024-06-18','13.0','CLI016'),
(17,'234.60','2024-06-25','15.6','CLI017'),(18,'95.75','2024-07-03','8.0','CLI018'),
(19,'267.50','2024-07-12','17.8','CLI019'),(20,'78.90','2024-07-20','6.6','CLI020'),
(21,'145.20','2024-08-02','9.7','CLI001'),(22,'189.00','2024-08-15','12.6','CLI003'),
(23,'112.50','2024-08-28','9.4','CLI005'),(24,'223.80','2024-09-10','14.9','CLI007'),
(25,'97.50','2024-09-22','8.1','CLI009');


INSERT INTO ACHAT_VETEMENT VALUES
('AV001','3.5'),('AV002','2.8'),('AV003','4.2'),('AV004','1.9'),('AV005','5.1'),
('AV006','3.3'),('AV007','6.0'),('AV008','2.5'),('AV009','4.7'),('AV010','1.8'),
('AV011','3.9'),('AV012','2.6'),('AV013','7.2'),('AV014','2.1'),('AV015','4.5'),
('AV016','3.7'),('AV017','5.8'),('AV018','2.3'),('AV019','6.5'),('AV020','2.0'),
('AV021','3.1'),('AV022','4.9'),('AV023','2.7'),('AV024','5.5'),('AV025','2.4'),
('AV026','4.1'),('AV027','3.6'),('AV028','5.3'),('AV029','2.9'),('AV030','4.8');


INSERT INTO Asso_14 VALUES
('CAT001','AV001'),('CAT002','AV002'),('CAT003','AV003'),('CAT004','AV004'),('CAT005','AV005'),
('CAT006','AV006'),('CAT007','AV007'),('CAT008','AV008'),('CAT009','AV009'),('CAT010','AV010'),
('CAT001','AV011'),('CAT002','AV012'),('CAT003','AV013'),('CAT004','AV014'),('CAT005','AV015'),
('CAT006','AV016'),('CAT007','AV017'),('CAT008','AV018'),('CAT009','AV019'),('CAT010','AV020'),
('CAT001','AV021'),('CAT003','AV022'),('CAT005','AV023'),('CAT007','AV024'),('CAT009','AV025'),
('CAT002','AV026'),('CAT004','AV027'),('CAT006','AV028'),('CAT008','AV029'),('CAT010','AV030');


INSERT INTO Asso_15 VALUES
(1,'AV001'),(1,'AV002'),(2,'AV003'),(3,'AV004'),(3,'AV005'),(4,'AV006'),
(5,'AV007'),(5,'AV008'),(6,'AV009'),(7,'AV010'),(7,'AV011'),(8,'AV012'),
(9,'AV013'),(9,'AV014'),(10,'AV015'),(11,'AV016'),(12,'AV017'),(12,'AV018'),
(13,'AV019'),(13,'AV020'),(14,'AV021'),(15,'AV022'),(16,'AV023'),(16,'AV024'),
(17,'AV025'),(18,'AV026'),(19,'AV027'),(19,'AV028'),(20,'AV029'),(21,'AV030');

-- R1-COLLECTE VETEMENT
SELECT date_collecte, quantite_vetement
FROM COLLECTE_VETEMENT;

-- R2
SELECT COLLECTE_VETEMENT.date_collecte, COLLECTE_VETEMENT.quantite_vetement
FROM COLLECTE_VETEMENT
WHERE (date_collecte LIKE '%01%');

-- R3
SELECT CV.date_collecte, CV.quantite_vetement, CAT.nom_vetement
FROM COLLECTE_VETEMENT as CV
INNER JOIN CATEGORIE_VETEMENTS CAT ON CV.categorie_vetement_id = CAT.id_categorie_vetement
WHERE nom_vetement = 'T-shirt';


-- R1-ACHAT VETEMENT
SELECT AV.id_achat_vetement, AV.quantite_achete, A15.id_achat
FROM ACHAT_VETEMENT as AV
INNER JOIN Asso_15 A15 ON AV.id_achat_vetement = A15.id_achat_vetement;


 -- R2
SELECT AV.quantite_achete, CV.nom_vetement
FROM ACHAT_VETEMENT as AV
INNER JOIN Asso_14 A14 ON AV.id_achat_vetement = A14.id_achat_vetement
INNER JOIN CATEGORIE_VETEMENTS as CV ON A14.id_categorie_vetement = CV.id_categorie_vetement;

-- R3
SELECT AV.quantite_achete, AV.id_achat_vetement
FROM ACHAT_VETEMENT as AV
ORDER BY AV.quantite_achete ASC;

-- R1 DEPOSE
SELECT c.nom, c.prénom, COUNT(d.num_depot) AS nombre_deposes
FROM CLIENT as c
JOIN Asso_8 a8 ON c.id_client = a8.id_client
JOIN DEPOSE d ON a8.num_depot = d.num_depot
GROUP BY c.nom, c.prénom
ORDER BY nombre_deposes DESC;

-- R2
SELECT cv.nom_vetement, COUNT(d.num_depot) AS nombre_deposes
FROM CATEGORIE_VETEMENTS as cv
JOIN Asso_9 a9 ON cv.id_categorie_vetement = a9.id_categorie_vetement
JOIN DEPOSE d ON a9.num_depot = d.num_depot
GROUP BY cv.nom_vetement
ORDER BY nombre_deposes DESC;

-- R3

SELECT  MONTH(date_depot) AS mois, COUNT(num_depot) AS nombre_deposes
FROM DEPOSE
GROUP BY MONTH(date_depot)
ORDER BY mois;

-- R1 ACHAT Lister les client ayant plus de 500 points de fidelité.
SELECT c.nom, c.email, c.point_fidelite
FROM CLIENT c
WHERE point_fidelite > 500
ORDER BY point_fidelite;

-- R2 Lister les clients et le montant total de leurs achats
SELECT c.id_client, c.nom, c.prénom, a.montant_total
FROM CLIENT c
JOIN ACHAT a ON c.id_client = a.client_id;

-- R3 Afficher les clients et le poids total de vêtements achetés.
SELECT  c.id_client, c.nom, c.prénom, SUM(av.quantite_achete) AS total_kg_achetes
FROM CLIENT c
JOIN ACHAT a ON c.id_client = a.client_id
JOIN Asso_15 a15 ON a.id_achat = a15.id_achat
JOIN ACHAT_VETEMENT av ON a15.id_achat_vetement = av.id_achat_vetement
GROUP BY c.id_client, c.nom, c.prénom
ORDER BY total_kg_achetes DESC;