# lotsOfTripsProject
Lots-Of-Trips: automated public transportation system.
 The system is built as client(s) – server system. Clients send requests to 
the server and receive a relevant answer. Thus, the request considered as 
satisfied.
 Objects of the system are magnetic cards that stored as records in SQL 
table on server-side. Each card has its unique ID number (four digits at 
most), contract and wallet fields.
 There are 4 types of contracts: North, Center, South and None.
 The value of the wallet is integer, non-negative number.
 Client allowed to receive followed services:
0. Before satisfaction of each potential request, the server or the client 
checks the card’s legality. In case that there is no such card in the 
dataset or in the collection respectively, a relevant message is shown 
and request is rejected. 
1. Create a new card. The client requests it and the server returns back 
the ID of the newly created card. The default value of the card’s wallet 
is 0 and the contract is None.
2. Check the status of an existed card. The client asks for information
about the existed card, mentions its ID and receives the data: a wallet 
and a contract values.
3. Pay for a ride. The client is interested in payment, mentions card’s ID, 
region of the destination and receives two possible answers: Done in 
case that ride is allowed or None otherwise.
There are two possibilities to pay for a ride: using wallet or using 
contract.
  a) In the first case, there are predefined prices for each one of 
  regions: the ride in the north costs 25, center – 40, south – 30.
  b) In case of using the contract, the clients allowed to ride with no 
  payment at all only in region mentioned in contract field, 
  nevertheless, if the client decides to take a ride to different that 
  mentioned in contract region the payment will be automatically 
  redirected to wallet. Further actions occur according to the using
  wallet option scenario.
4. Fill/Refill the wallet. The client wants to increase a value of the wallet. It 
requires mentioning card’s ID and the sum to add to wallet value. In 
case that the value is logically correct (you can assume that the 
maximum sum of refill at one time is 4-digit number), the server notifies 
the client about success by sending Done, otherwise – client sends Fail
as response.
5. Exchange/Change the contract. The client decides to 
change/exchange the contract, mentions card’s ID and the name of the 
contract. In case that the value is logically correct, the server notifies 
the client about success, otherwise – the message about a failure is 
sent back.
6. Also, there is an option to see IDs of all cards.
