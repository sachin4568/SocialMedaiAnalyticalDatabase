# Social Media Analytical Database with SNM Integration

## Setup Instructions

### Backend

1. Install MySQL and create database:

```sql
CREATE DATABASE socialdb;
USE socialdb;

CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Age INT,
    Gender VARCHAR(10),
    Location VARCHAR(100)
);

CREATE TABLE Post (
    PostID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Content TEXT,
    Timestamp DATETIME,
    SentimentScore FLOAT,
    FOREIGN KEY (User ID) REFERENCES User(UserID)
);

CREATE TABLE Follow (
    FollowerID INT,
    FollowingID INT,
    Timestamp DATETIME,
    PRIMARY KEY (FollowerID, FollowingID),
    FOREIGN KEY (FollowerID) REFERENCES User(UserID),
    FOREIGN KEY (FollowingID) REFERENCES User(UserID)
);



---

## Final notes

- After creating these files and folders, run backend and frontend as described.
- You can zip the whole `social-media-analytical-db` folder for backup or sharing.
- If you want, I can help you with any step or provide scripts to automate setup.

---

If you want, I can also generate a single downloadable archive with these files and provide a link via a file-sharing service. Just let me know!