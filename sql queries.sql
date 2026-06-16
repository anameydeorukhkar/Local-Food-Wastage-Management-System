BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "claims" (
	"Claim_ID"	INTEGER,
	"Food_ID"	INTEGER,
	"Receiver_ID"	INTEGER,
	"Status"	TEXT,
	"Timestamp"	TEXT,
	PRIMARY KEY("Claim_ID"),
	FOREIGN KEY("Food_ID") REFERENCES "food_listings"("Food_ID"),
	FOREIGN KEY("Receiver_ID") REFERENCES "receivers"("Receiver_ID")
);
CREATE TABLE IF NOT EXISTS "food_listings" (
	"Food_ID"	INTEGER,
	"Food_Name"	TEXT,
	"Quantity"	INTEGER,
	"Expiry_Date"	TEXT,
	"Provider_ID"	INTEGER,
	"Provider_Type"	TEXT,
	"Location"	TEXT,
	"Food_Type"	TEXT,
	"Meal_Type"	TEXT,
	PRIMARY KEY("Food_ID"),
	FOREIGN KEY("Provider_ID") REFERENCES "providers"("Provider_ID")
);
CREATE TABLE IF NOT EXISTS "providers" (
	"Provider_ID"	INTEGER,
	"Name"	TEXT,
	"Type"	TEXT,
	"Address"	TEXT,
	"City"	TEXT,
	"Contact"	TEXT,
	PRIMARY KEY("Provider_ID")
);
CREATE TABLE IF NOT EXISTS "receivers" (
	"Receiver_ID"	INTEGER,
	"Name"	TEXT,
	"Type"	TEXT,
	"City"	TEXT,
	"Contact"	TEXT,
	PRIMARY KEY("Receiver_ID")
);
COMMIT;
