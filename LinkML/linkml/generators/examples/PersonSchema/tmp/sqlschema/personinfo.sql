

CREATE TABLE "Nationaliteit" (
	nationaliteit TEXT, 
	PRIMARY KEY (nationaliteit)
);

CREATE TABLE "Person" (
	achternaam TEXT, 
	"alternatieveNaam" TEXT, 
	contactinfo TEXT NOT NULL, 
	geboortenaam TEXT, 
	"gebruikteVoornaam" TEXT, 
	geslacht TEXT, 
	patroniem TEXT, 
	"volledigeNaam" TEXT, 
	voornaam TEXT, 
	PRIMARY KEY (achternaam, "alternatieveNaam", contactinfo, geboortenaam, "gebruikteVoornaam", geslacht, patroniem, "volledigeNaam", voornaam)
);
