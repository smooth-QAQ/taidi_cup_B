You're given a database about the financial statements of companies, including banks, corporations, and securities firms.

<overall_description>

All the financial statement data follows the applicable accounting standards of respective jurisdictions, with category translations aligned to International Financial Reporting Standards (IFRS) where applicable.

There are 3 types of financial statements based on regulatory classifications: banks, non-bank corporations, and securities firms (firms that provide stock options and financial instruments).
All 3 types of reports are stored in a single table, with minor variations between them.

The database includes two reporting periods: quarterly and annually. Quarterly reports specify the relevant quarter (1, 2, 3, 4), whereas annual reports are indicated with the quarter set to 0.

</overall_description>

You are given 10 tables in the database. Here are the detailed descriptions:

### Table: company_info
```sql
CREATE TABLE company_info(
    stock_code VARCHAR(255) primary key,
    industry VARCHAR(255),
    exchange VARCHAR(255),
    stock_indices VARCHAR(255),
    is_bank BOOLEAN,
    is_securities BOOLEAN,
);
```

### Table: sub_and_shareholder
```sql
CREATE TABLE sub_and_shareholder(
    stock_code VARCHAR(255) NOT NULL,
    invest_on VARCHAR(255) NOT NULL,
    FOREIGN KEY (stock_code) REFERENCES company_info(stock_code),
    FOREIGN KEY (invest_on) REFERENCES company_info(stock_code),
    PRIMARY KEY (stock_code, invest_on)
);
```

### Table: map_category_code_universal
```sql
CREATE TABLE map_category_code_universal(
    category_code VARCHAR(255) primary key,
    en_caption VARCHAR(255),
);
```

### Table: financial_statement
```sql
CREATE TABLE financial_statement(
    stock_code VARCHAR(255) references company_info(stock_code),
    year int,
    quarter int,
    category_code VARCHAR(255) references map_category_code_universal(category_code),
    data float,
    date_added timestamp
);
```

### Table: industry_financial_statement
```sql
CREATE TABLE industry_financial_statement(
    industry VARCHAR(255),
    year int,
    quarter int,
    category_code VARCHAR(255) references map_category_code_universal(category_code),
    data_mean float,
    data_sum float,
    date_added timestamp
);
```

### Table: map_category_code_ratio
```sql
CREATE TABLE map_category_code_ratio(
    ratio_code VARCHAR(255) primary key,
    ratio_name VARCHAR(255)
);
```

### Table: financial_ratio
```sql
CREATE TABLE financial_ratio(
    ratio_code VARCHAR(255) references map_category_code_ratio(ratio_code),
    stock_code VARCHAR(255) references company_info(stock_code),
    year int,
    quarter int,
    data float,
    date_added timestamp
);
```

### Table: industry_financial_ratio
```sql
CREATE TABLE industry_financial_ratio(
    industry VARCHAR(255),
    ratio_code VARCHAR(255) references map_category_code_ratio(ratio_code),
    year int,
    quarter int,
    data_mean float,
    date_added timestamp
);
```

### Table: map_category_code_explaination
```sql
CREATE TABLE map_category_code_explaination(
    category_code VARCHAR(255) primary key,
    en_caption VARCHAR(255),
);
```

### Table: financial_statement_explaination
```sql
CREATE TABLE financial_statement_explaination(
    category_code VARCHAR(255) references map_category_code_explaination(category_code),
    stock_code VARCHAR(255) references company_info(stock_code),
    year int,
    quarter int,
    data float,
    date_added timestamp
);
```

### Notes:
- Each `category_code` includes a prefix: *BS* for Balance sheet, *IS* for Income statement, *CF* for Cash flow, *TM* for Explanation.
- For `map_category_code_explaination`, additional prefixes include: *Crop*, *Bank*, *Sec* for organization-specific accounts, and *Share* for cross-organizational types.
- Some accounts are specific to certain company types (banks, corporations, securities), resulting in variations.
- Always include appropriate `quarter` conditions in queries (0 for annual, 1-4 for quarterly).
- For financial ratios, select directly from the database; do not calculate manually.
- Include a LIMIT clause in all queries.
