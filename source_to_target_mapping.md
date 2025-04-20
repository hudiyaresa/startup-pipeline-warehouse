**Source-to-Target Mapping (STM)** between the raw source tables and the final cleaned/structured **target schema**.


## 1. `company` Table Mapping

| Target Column      | Source Column           | Transformation / Notes                                     |
|--------------------|-------------------------|-------------------------------------------------------------|
| object_id          | object_id       | Keep as is (PK in target)                                   |
| description        | description     | Keep as is                                                  |
| region             | region          | Keep as is                                                  |
| address1           | address1        | Keep as is                                                  |
| address2           | address2        | Keep as is                                                  |
| city               | city            | Keep as is                                                  |
| zip_code           | zip_code        | Truncate or cast to VARCHAR(20)                             |
| state_code         | state_code      | Truncate or cast to VARCHAR(10)                             |
| country_code       | country_code    | Truncate or cast to VARCHAR(10)                             |
| latitude           | latitude        | Cast to FLOAT                                               |
| longitude          | longitude       | Cast to FLOAT                                               |
| created_at         | created_at      | Keep as is                                                  |
| updated_at         | updated_at      | Keep as is                                                  |

---

## 2. `acquisition` Table Mapping

| Target Column        | Source Column                 | Transformation / Notes                                     |
|----------------------|-------------------------------|-------------------------------------------------------------|
| acquisition_id       | acquisition_id    | Keep as is                                                  |
| acquiring_object_id  | acquiring_object_id | Convert `character varying` to `INT` → Lookup from `object_id` |
| acquired_object_id   | acquired_object_id | Same as above                                               |
| term_code            | term_code         | Truncate to VARCHAR(50)                                     |
| price_amount         | price_amount      | Keep as is                                                  |
| price_currency_code  | price_currency_code | Expand VARCHAR(3) → VARCHAR(10)                            |
| acquired_at          | acquired_at       | Convert `timestamp` to `DATE`                              |
| source_url           | source_url        | Truncate to 255 chars                                       |
| source_description   | source_description| Keep as is                                                  |
| created_at           | created_at        | Keep as is                                                  |
| updated_at           | updated_at        | Keep as is                                                  |

---

## 3. `funding_rounds` Table Mapping

| Target Column             | Source Column                      | Transformation / Notes                                                |
|---------------------------|------------------------------------|------------------------------------------------------------------------|
| funding_round_id          | funding_round_id    | Keep as is                                                             |
| object_id                 | object_id           | Convert `character varying` to `INT` → Lookup from `object_id`|
| funded_at                 | funded_at           | Keep as is                                                             |
| funding_round_type        | funding_round_type  | Truncate to VARCHAR(50)                                               |
| funding_round_code        | funding_round_code  | Truncate to VARCHAR(50)                                               |
| raised_amount_usd         | raised_amount_usd   | Keep as is                                                             |
| raised_amount             | raised_amount       | Keep as is                                                             |
| raised_currency_code      | raised_currency_code| Truncate to VARCHAR(10)                                               |
| pre_money_valuation_usd   | pre_money_valuation_usd | Keep as is                                                         |
| pre_money_valuation       | pre_money_valuation | Keep as is                                                             |
| post_money_valuation_usd  | post_money_valuation_usd | Keep as is                                                       |
| post_money_valuation      | post_money_valuation | Keep as is                                                             |
| post_money_currency_code  | post_money_currency_code | Truncate to VARCHAR(10)                                           |
| participants              | participants        | Might need transformation → Convert text to INT (count, if possible) |
| is_first_round            | is_first_round      | Keep as is                                                             |
| is_last_round             | is_last_round       | Keep as is                                                             |
| source_url                | source_url          | Truncate if needed                                                    |
| source_description        | source_description  | Keep as is                                                             |
| created_by                | created_by          | Keep as is                                                             |
| created_at                | created_at          | Keep as is                                                             |
| updated_at                | updated_at          | Keep as is                                                             |

---

## 4. `ipos` Table Mapping

| Target Column          | Source Column              | Transformation / Notes                                    |
|------------------------|----------------------------|------------------------------------------------------------|
| object_id              | object_id             | Convert from VARCHAR → INT (lookup from `object_id`) |
| valuation_amount       | valuation_amount      | Keep as is                                                 |
| valuation_currency_code| valuation_currency_code| Truncate if needed                                         |
| raised_amount          | raised_amount         | Keep as is                                                 |
| raised_currency_code   | raised_currency_code  | Truncate if needed                                         |
| public_at              | public_at             | Convert TIMESTAMP → DATE                                   |
| stock_symbol           | stock_symbol          | Truncate to 20 chars                                       |
| source_url             | source_url            | Truncate if needed                                         |
| source_description     | source_description    | Keep as is                                                 |
| created_at             | created_at            | Keep as is                                                 |
| updated_at             | updated_at            | Keep as is                                                 |

---

## 5. `funds` Table Mapping

| Target Column         | Source Column             | Transformation / Notes                                       |
|-----------------------|---------------------------|---------------------------------------------------------------|
| fund_id               | fund_id             | Convert VARCHAR → INT (needs surrogate key or sequence)       |
| object_id             | object_id           | Lookup object_id and convert to INT                   |
| name                  | name                | Keep as is                                                    |
| funded_at             | funded_at           | Keep as is                                                    |
| raised_amount         | raised_amount       | Keep as is                                                    |
| raised_currency_code  | raised_currency_code| Truncate to 10 chars                                          |
| source_url            | source_url          | Truncate if needed                                            |
| source_description    | source_description  | Keep as is                                                    |
| created_at            | created_at          | Keep as is                                                    |
| updated_at            | updated_at          | Keep as is                                                    |

---

## 6. `investments` Table Mapping

| Target Column       | Source Column               | Transformation / Notes                                          |
|---------------------|-----------------------------|------------------------------------------------------------------|
| investment_id       | investment_id   | Keep as is                                                       |
| funding_round_id    | funding_round_id| Keep as is                                                       |
| funded_object_id    | funded_object_id| Convert from VARCHAR → INT (lookup from `object_id`)     |
| investor_object_id  | investor_object_id| Convert from VARCHAR → INT (lookup from `object_id`)   |
| created_at          | created_at      | Keep as is                                                       |
| updated_at          | updated_at      | Keep as is                                                       |

---

## 7. Others (people, relationships, milestones)

These are not included in the target schema:

- **people**: Could be a `person` table (not in target yet)
- **relationships**: Could relate to employment history, roles → `person_company_relationship` table
- **milestones**: Business events, news mentions → perhaps `company_milestones` table in future schema

---


1. **ID Conversion**: Most object IDs in the source are strings like `c:123`, `p:2`. You’ll need to **extract the numeric part and typecast to INT** for the target.
   - Use regex or string split:
     ```sql
     CAST(SPLIT_PART(object_id, ':', 2) AS INTEGER)
     ```

---
