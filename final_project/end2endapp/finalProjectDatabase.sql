USE finalProject;
CREATE TABLE example_table (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    age INT,
    primary key (id)
);

create table customer (
	dob VARCHAR(20) NOT NULL,
	enitity VARCHAR(32) NOT NULL,
    ssn int primary key,
    cusimage VARCHAR(16) NOT NULL,
    rssn int,
    foreign key (rssn) references customer(ssn)
);

create table Account(
	AccountIDNumber int primary key,
    LocationAddress VARCHAR(255),
    AccountName VARCHAR(32),
    AccountRelation VARCHAR(32)
);

create table hasAccount (
	AccountID int,
    ssn int,
    foreign key (ssn) references customer(ssn),
    foreign key (AccountID) references Account(AccountIDNumber)
);

create table billingAccount(
	billingAccountID int primary key,
    BAccName VARCHAR(32),
    billingAddress VARCHAR(255)
);

create table AccountAdmin(
	AdminName VARCHAR(32) primary key,
    AdminAddress VARCHAR(255)
);

create table billingAccount_Admin(
	billingAccountID int primary key,
    AdminName VARCHAR(32),
    foreign key (billingAccountID) references billingAccount(billingAccountID),
    foreign key(AdminName) references AccountAdmin(AdminName)
);


create table AccountAlias(
	AliasID int primary key,
    AliasSource VARCHAR(32),
    AccountIDNumber int,
    foreign key(AccountIDNumber) references Account(AccountIDNumber)
);

create table Acc_Admin(
	AccountIDNumber int,
    AdminName VARCHAR(32),
    foreign key(AccountIDNumber) references Account(AccountIDNumber),
    foreign key(AdminName) references AccountAdmin(AdminName)
);

create table AcctBillingAccount(
	AccountIDNumber int primary key,
    billingAccountID int,
    relationshipType VARCHAR(32),
    StartDate VARCHAR(32),
    foreign key(AccountIDNumber) references Account(AccountIDNumber),
    foreign key(billingAccountID) references billingAccount(billingAccountID)
);

create table ManagerContract(
	SitCode int primary key,
    IssueDate VARCHAR(32)
); 

create table Account_ManagerCont(
	AccountIDNumber int,
    SitCode int,
    AssociateType VARCHAR(32),
	foreign key(AccountIDNumber) references Account(AccountIDNumber),
	foreign key(SitCode) references ManagerContract(SitCode)
);  

create table Associate(
	AssocName VARCHAR(32) primary key,
    AssocDOB VARCHAR(20) NOT NULL,
    Assoc_office VARCHAR(32),
    RAssocName VARCHAR(32),
	foreign key (RAssocName) references Associate(AssocName)
);

create table Asso_ManagerCon(
	AssocName VARCHAR(32),
    SitCode int,
    Writing_Number int primary key,
	foreign key (AssocName) references Associate(AssocName),
    foreign key(SitCode) references ManagerContract(SitCode)
); 

create table Contract(
	ContractNumber int primary key,
    Seller VARCHAR(32),
    SeriesName VARCHAR(64),
    PlanName VARCHAR(64)
);

create table LegacyPolicy_Account(
	ContractNumber int,
    AliasID int,
    foreign key (ContractNumber) references Contract(ContractNumber),
    foreign key (AliasID) references AccountAlias(AliasID)
); 

create table ContractBenefit(
	Benefit_code int primary key,
    Benefit_policy VARCHAR(64),
    ContractNumber int,
    foreign key (ContractNumber) references Contract(ContractNumber)
); 

create table ContractPremium(
	Premium_code int primary key,
    Benefit_policy VARCHAR(64),
    Benefit_code int,
    foreign key (Benefit_code) references ContractBenefit(Benefit_code)
); 

create table ContractPartyRole(
	ContractNumber int,
    ssn int,
    lifePolicy VARCHAR(64),
    foreign key (ContractNumber) references Contract(ContractNumber),
	foreign key (ssn) references customer(ssn)
); 

create table CusContBenefit(
	Benefit_code int,
    ssn int,
    foreign key (Benefit_code) references ContractBenefit(Benefit_code),
	foreign key (ssn) references customer(ssn)
); 

create table Premium_MgmtContract(
	Premium_code int,
    SitCode int,
    foreign key (Premium_code) references ContractPremium(Premium_code),
	foreign key(SitCode) references ManagerContract(SitCode)
); 
