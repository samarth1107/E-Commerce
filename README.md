# iMart (E-Commerce website)

An e-commerce website is a software system developed primarily to facilitate buying and selling of products between users.  

This website has primarily 3 stakeholders user, seller and site admin.


User guide is available [here](https://github.com/samarth1107/E-Commerce/blob/main/UserGuide.pdf)


### Users 
In this project, there are following categories of users: 
1.  Buyers 

A buyer is a free user of this service. A buyer will signup and login to the system to get access to a catalog of products. The products can belong to categories, and the user can search for specific products on the website.

A product will have at least two images, a name and a description. You can add additional information, if required.

A buyer can also purchase a product. To mimic a payment gateway, you can use stripe in test mode. It is easy to set up and allows transactions from a dummy card in dev mode. You can skip stripe integration if it gets too difficult, and create a simple CRUD based simple payment gateway as well.


2. Sellers
A seller will request the admin for approval of selling. The seller will have to upload a document (can be any pdf) and send it to the admin for approval. 
Once a seller has approval from the admin, they will be allowed to catalog products, set the inventory, add product details, and so on. 

3. Admin 

An admin can remove any suspicious buyers or sellers from the e-commerce system. They can approve seller applications after looking at the documents. They can add or remove any products listed by any seller. 


### Functionality 

• General functionality details: Below are some general functionality details which  should be implemented. 

a. Mechanism to search products using name, category, etc.

b. Creation and Maintenance of product list 

c. Ability to set/edit settings 

d. An e-cash wallet (or a payment gateway) for performing financial transactions. 

e. Maintenance of profile information of the user. 

f. Ability to share, sell and purchase products

g. Admin capabilities as mentioned above or more

h. Seller-Admin approval process using a document upload.

i. Key Certificates: The secure e-commerce website must use public  key infrastructure (PKI) in addition to using SSL/TSL (HTTPS) to enforce the  security of the application. You can establish your own certificate issuing  authority for the purpose of this project. A minimum of two functions must employ  PKI, and you may decide the extent of the PKI applicability to the functions.  

j. OTP: The secure e-commerce website must employ OTP (One Time  Password) technique with virtual keyboard feature to validate highly sensitive  transactions for at least two of the functions in requirements. You may decide the  extent of the OTP applicability to the functions.  

k. The secure e-commerce website should allow multiple users to use the  system simultaneously. 

l. Secure transaction logging is required to enable external audits. 

m. Security features to defend against attacks on the secure  e-commerce website.

