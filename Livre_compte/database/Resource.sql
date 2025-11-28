drop database if exists livrecompte;
create database if not exists livrecompte;

use livrecompte;

create table if not exists branche(
	id int not null primary key auto_increment,
	nom varchar(50)
);

create table if not exists argent_depense(
	id int not null primary key auto_increment,
	designation text not null,
	montant double not null,
	date_sortie date not null,
	id_branche int not null,
	foreign key(id_branche) references branche(id)
);

create table if not exists argent_entrer(
	id int not null primary key auto_increment,
	designation text not null,
	montant double not null,
	date_entre date not null,
	id_branche int not null,
	foreign key(id_branche) references branche(id)
);
