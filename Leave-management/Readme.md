Assignment : Employee Leave Management System

1. Database-schema: Prepared a database name “leave_management” that consists of all the related tables for this assignment. Implemented model file which gives the overview of the columns present in the particular table. Implement hashing password with the help of “bcrypt” which is stored in the database. All the models are implemented using pydantic validations.

2. Routers: Work on three routers 1. Auth,  2. Employee, 3. Leaves. Auth router used for getting the jwt token to authenticate the employee. Only authenticated employees can apply for leave. An employee router considers two types of roles.  One is an employee and the other one is a manager. Only managers can have the access to list all the employees and to add a new employee.

3. Leaves: Employees can apply for leave and can view their list of requests.  Managers can view the pending request and can approve or reject the request. Employees can check their leave balance after applying for the leave. 

4. Validations: Implemented some validations like start date and end date cannot be before created leave requests date. Employees cannot apply for the leave if leave balance is not sufficient. 