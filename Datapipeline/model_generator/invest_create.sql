
CREATE TABLE Company (
    id bigserial  NOT NULL,
    Country varchar(50)  NOT NULL,
    Date timestamp(20)  NOT NULL,
    Price decimal(10,5)  NOT NULL,
    Open decimal(10,5)  NOT NULL,
    High decimal(10,5)  NOT NULL,
    Low decimal(10,5)  NOT NULL,
    Volume bigint  NOT NULL,
    Change decimal(5,4)  NOT NULL,
    CONSTRAINT Company_pk PRIMARY KEY (id)
);


