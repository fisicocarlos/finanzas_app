CREATE TABLE IF NOT EXISTS "types" (
    "type_id" SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE,
    "date_created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "date_modified" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT
);

CREATE TABLE categories (
    "category_id" SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE,
    "type_id_default" BIGINT,
    "color" TEXT,
    "icon_path" TEXT,
    "icon_char" TEXT,
    "description" TEXT,
    "notes" TEXT,
    "date_created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "date_modified" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id_default) REFERENCES types(type_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "trips" (
    "trip_id" SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE,
    "date_start" DATE,
    "date_end" DATE,
    "description" TEXT,
    "color" TEXT,
    "date_created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "date_modified" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS "transactions" (
    "id" SERIAL PRIMARY KEY,
    "date" DATE NOT NULL,
    "description" TEXT NOT NULL,
    "type_id" BIGINT,
    "amount" NUMERIC(12, 2) NOT NULL,
    "category_id" BIGINT,
    "trip_id" BIGINT,
    "notes" TEXT,
    "date_created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "date_modified" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("trip_id") REFERENCES "trips"("trip_id") ON UPDATE NO ACTION ON DELETE SET NULL,
    FOREIGN KEY("category_id") REFERENCES "categories"("category_id") ON UPDATE NO ACTION ON DELETE SET NULL,
    FOREIGN KEY("type_id") REFERENCES "types"("type_id") ON UPDATE NO ACTION ON DELETE NO ACTION
);


CREATE OR REPLACE FUNCTION update_date_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_modified = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_types
BEFORE UPDATE ON types
FOR EACH ROW
EXECUTE FUNCTION update_date_modified();

CREATE TRIGGER trg_update_categories
BEFORE UPDATE ON categories
FOR EACH ROW
EXECUTE FUNCTION update_date_modified();

CREATE TRIGGER trg_update_trips
BEFORE UPDATE ON trips
FOR EACH ROW
EXECUTE FUNCTION update_date_modified();

CREATE TRIGGER trg_update_transactions
BEFORE UPDATE ON transactions
FOR EACH ROW
EXECUTE FUNCTION update_date_modified();
