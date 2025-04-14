Fight Booking  Systems 

Technology Stack Used 
● Backend Framework: Django (Python) 
● Frontend: HTML, CSS, Bootstrap, JavaScript 
● Database: MySQL or SQLite (during development) 
● Authentication: Django's built-in user model 
● Image Uploads: Django ImageField for airlines and airports 
● Payment Logic: Simulated using Django models

Data Flow Examples: 
● User inputs login → Authentication Process → Validate using User DB 
● User searches for flights → Search Process → Flight DB → Results 
● User books flight → Booking Process → Store in Booking DB 
● Admin updates flight → Admin Panel → Update Flight DB 
● Booking → Payment → Store in Payment DB and return status
