# Entity relationship model

```mermaid
erDiagram
  CUSTOMER_PURCHASES {
    INTEGER customerid PK
    TEXT name
    INTEGER age
    REAL purchaseamount
    TEXT country
    TEXT date
    TEXT age_group
    TEXT purchase_category
    INTEGER purchase_year
  }
```

One synthetic purchase per CustomerID is generated for this teaching example. CustomerID is unique. A production system would separate customers and purchases into two tables with a one-to-many relationship.
