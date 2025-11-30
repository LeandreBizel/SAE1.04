DROP TABLE IF EXISTS RECUPERE;
DROP TABLE IF EXISTS ASSOCIEA;
DROP TABLE IF EXISTS DISTANCE_ENTRE;
DROP TABLE IF EXISTS ACHAT_VETEMENT;
DROP TABLE IF EXISTS COLLECTE_VETEMENT;
DROP TABLE IF EXISTS DEPOSE;
DROP TABLE IF EXISTS DEPOT;
DROP TABLE IF EXISTS ACHAT;
DROP TABLE IF EXISTS CAMIONETTE;
DROP TABLE IF EXISTS COLLECTE;
DROP TABLE IF EXISTS BENNE;
DROP TABLE IF EXISTS CATEGORIE_VETEMENTS;
DROP TABLE IF EXISTS CLIENT;


CREATE TABLE CLIENT(
    id_client INT AUTO_INCREMENT,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    adresse VARCHAR(100),
    telephone VARCHAR(15),
    email VARCHAR(100),
    total_kg_achetes DECIMAL(10,2) DEFAULT 0,
    date_1ere_achat DATE,
    point_fidelite INT DEFAULT 0,
    PRIMARY KEY(id_client)
);

CREATE TABLE CATEGORIE_VETEMENTS(
    id_categorie_vetement INT AUTO_INCREMENT,
    nom_vetement VARCHAR(50),
    prix_kg DECIMAL(10,2),
    PRIMARY KEY(id_categorie_vetement)
);

CREATE TABLE BENNE(
    id_benne INT AUTO_INCREMENT,
    adresse_benne VARCHAR(100),
    distance_magasin DECIMAL(10,2),
    coordonnees_gps VARCHAR(50),
    PRIMARY KEY(id_benne)
);

CREATE TABLE COLLECTE(
    id_collecte INT AUTO_INCREMENT,
    date_collecte DATE,
    duree_collecte TIME,
    PRIMARY KEY(id_collecte)
);

CREATE TABLE CAMIONETTE(
    id_camionette INT AUTO_INCREMENT,
    immatriculation VARCHAR(20),
    capacite_max DECIMAL(10,2),
    PRIMARY KEY(id_camionette)
);

CREATE TABLE ACHAT(
    id_achat INT AUTO_INCREMENT,
    montant_total DECIMAL(10,2) NOT NULL,
    date_achat DATE,
    poids_total DECIMAL(10,2),
    client_id INT,
    PRIMARY KEY(id_achat),
    FOREIGN KEY(client_id) REFERENCES CLIENT(id_client)
);

CREATE TABLE DEPOT(
    id_depot INT AUTO_INCREMENT,
    PRIMARY KEY(id_depot)
);

CREATE TABLE DEPOSE(
    num_depot INT AUTO_INCREMENT,
    quantite_depot DECIMAL(10,2),
    date_depot DATE,
    id_depot INT NOT NULL,
    id_categorie_vetement INT NOT NULL,
    id_client INT NOT NULL,
    PRIMARY KEY(num_depot),
    FOREIGN KEY(id_depot) REFERENCES DEPOT(id_depot),
    FOREIGN KEY(id_categorie_vetement) REFERENCES CATEGORIE_VETEMENTS(id_categorie_vetement),
    FOREIGN KEY(id_client) REFERENCES CLIENT(id_client)
);

CREATE TABLE COLLECTE_VETEMENT(
    id_collecte_vetement INT AUTO_INCREMENT,
    date_collecte DATE,
    quantite_vetement DECIMAL(10,2),
    id_collecte INT NOT NULL,
    id_categorie_vetement INT NOT NULL,
    PRIMARY KEY(id_collecte_vetement),
    FOREIGN KEY(id_collecte) REFERENCES COLLECTE(id_collecte),
    FOREIGN KEY(id_categorie_vetement) REFERENCES CATEGORIE_VETEMENTS(id_categorie_vetement)
);

CREATE TABLE ACHAT_VETEMENT(
    id_achat_vetement INT AUTO_INCREMENT,
    quantite_achete DECIMAL(10,2),
    achat_id INT NOT NULL,
    id_categorie_vetement INT NOT NULL,
    PRIMARY KEY(id_achat_vetement),
    FOREIGN KEY(achat_id) REFERENCES ACHAT(id_achat),
    FOREIGN KEY(id_categorie_vetement) REFERENCES CATEGORIE_VETEMENTS(id_categorie_vetement)
);

CREATE TABLE DISTANCE_ENTRE(
    id_benne INT,
    id_benne_1 INT,
    distance_inter_benne DECIMAL(10,2),
    PRIMARY KEY(id_benne, id_benne_1),
    FOREIGN KEY(id_benne) REFERENCES BENNE(id_benne),
    FOREIGN KEY(id_benne_1) REFERENCES BENNE(id_benne)
);

CREATE TABLE ASSOCIEA(
    id_collecte INT,
    id_camionette INT,
    PRIMARY KEY(id_collecte, id_camionette),
    FOREIGN KEY(id_collecte) REFERENCES COLLECTE(id_collecte),
    FOREIGN KEY(id_camionette) REFERENCES CAMIONETTE(id_camionette)
);

CREATE TABLE RECUPERE(
    id_benne INT,
    id_collecte INT,
    PRIMARY KEY(id_benne, id_collecte),
    FOREIGN KEY(id_benne) REFERENCES BENNE(id_benne),
    FOREIGN KEY(id_collecte) REFERENCES COLLECTE(id_collecte)
);


-- Clients
INSERT INTO CLIENT (nom, prenom, adresse, telephone, email, total_kg_achetes, date_1ere_achat, point_fidelite) VALUES
('Dupont', 'Marie', '12 rue de la Paix, Paris', '0612345678', 'marie.dupont@email.fr', 45.50, '2024-01-15', 455),
('Martin', 'Pierre', '8 avenue des Lilas, Lyon', '0623456789', 'pierre.martin@email.fr', 32.00, '2024-02-20', 320),
('Bernard', 'Sophie', '5 boulevard Victor Hugo, Marseille', '0634567890', 'sophie.bernard@email.fr', 67.80, '2023-12-10', 678),
('Petit', 'Luc', '3 place de la République, Toulouse', '0645678901', 'luc.petit@email.fr', 12.50, '2024-03-05', 125),
('Dubois', 'Emma', '15 rue du Commerce, Nantes', '0656789012', 'emma.dubois@email.fr', 89.20, '2023-11-22', 892);

-- Catégories de vêtements
INSERT INTO CATEGORIE_VETEMENTS (nom_vetement, prix_kg) VALUES
('T-shirts', 8.50),
('Jeans', 12.00),
('Pulls', 10.50),
('Robes', 15.00),
('Vestes', 18.00),
('Chemises', 9.50);

-- Bennes
INSERT INTO BENNE (adresse_benne, distance_magasin, coordonnees_gps) VALUES
('Place de la Gare, Paris 10e', 2.5, '48.8747,2.3570'),
('Parking Centre Commercial, Lyon 3e', 4.8, '45.7578,4.8320'),
('Rue des Docks, Marseille 2e', 3.2, '43.3047,5.3750'),
('Avenue Jean Jaurès, Toulouse', 5.1, '43.6045,1.4440'),
('Boulevard de la Prairie, Nantes', 1.9, '47.2184,-1.5536');

-- Collectes
INSERT INTO COLLECTE (date_collecte, duree_collecte) VALUES
('2024-11-01', '02:30:00'),
('2024-11-05', '03:15:00'),
('2024-11-10', '02:45:00'),
('2024-11-15', '03:00:00'),
('2024-11-20', '02:20:00');

-- Camionettes
INSERT INTO CAMIONETTE (immatriculation, capacite_max) VALUES
('AB-123-CD', 500.00),
('EF-456-GH', 600.00),
('IJ-789-KL', 550.00);

-- Achats
INSERT INTO ACHAT (montant_total, date_achat, poids_total, client_id) VALUES
(255.00, '2024-11-10', 15.50, 1),
(384.00, '2024-11-12', 32.00, 1),
(189.00, '2024-11-14', 18.00, 4),
(150.00, '2024-11-16', 12.50, 3),
(420.00, '2024-11-18', 28.00, 5);

-- Dépôts
INSERT INTO DEPOT VALUES
(1),
(2),
(3),
(4),
(5);

-- Déposés
INSERT INTO DEPOSE (quantite_depot, date_depot, id_depot, id_categorie_vetement, id_client) VALUES
(5.50, '2024-11-01', 1, 1, 1),
(8.00, '2024-11-02', 2, 2, 2),
(12.30, '2024-11-03', 3, 3, 3),
(6.50, '2024-11-04', 4, 4, 4),
(15.00, '2024-11-05', 5, 5, 5),
(7.20, '2024-11-06', 1, 6, 1),
(9.50, '2024-11-07', 2, 1, 3);

-- Collecte de vêtements
INSERT INTO COLLECTE_VETEMENT (date_collecte, quantite_vetement, id_collecte, id_categorie_vetement) VALUES
('2024-11-01', 45.50, 1, 1),
('2024-11-01', 32.00, 1, 2),
('2024-11-05', 28.50, 2, 3),
('2024-11-05', 41.20, 2, 4),
('2024-11-10', 35.80, 3, 5),
('2024-11-10', 22.50, 3, 6),
('2024-11-15', 38.00, 4, 1),
('2024-11-20', 47.30, 5, 2);

-- Achat de vêtements
INSERT INTO ACHAT_VETEMENT (quantite_achete, achat_id, id_categorie_vetement) VALUES
(8.50, 1, 1),
(7.00, 1, 2),
(15.00, 2, 3),
(17.00, 2, 4),
(10.00, 3, 5),
(8.00, 3, 6),
(12.50, 4, 1),
(15.50, 5, 2),
(12.50, 5, 3);

-- Distances entre bennes
INSERT INTO DISTANCE_ENTRE (id_benne, id_benne_1, distance_inter_benne) VALUES
(1, 2, 465.50),
(1, 3, 775.20),
(1, 4, 678.30),
(1, 5, 385.40),
(2, 3, 314.60),
(2, 4, 360.80),
(2, 5, 595.70),
(3, 4, 405.90),
(3, 5, 905.20),
(4, 5, 542.10);

-- Association collecte-camionette
INSERT INTO ASSOCIEA (id_collecte, id_camionette) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1),
(5, 2);

-- Récupération benne-collecte
INSERT INTO RECUPERE (id_benne, id_collecte) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3),
(5, 3),
(1, 4),
(2, 5),
(3, 5);