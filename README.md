# OTP GENERATION

### this file contains the two end points for otp generation and otp verification.

# endpoint-1:

/otp/send
The above end point will generate the OTP and it will return the user based on some third party services.

Here in the OTP generation we store our otp's in table for verify and we hash the our otp password.

# endpoint-2 

# /otp/verify

Whenever frontend request will comes user sends the OTP get from third party services.
 # there are some constraints to validate OTP.
  First one: If the user enter within the 2 minutes we can validate it is correct OTP otherwise we return it is invalid.
  Second one: Before check otp convert normal OTP to hash because in table we store in the hashing value.

# if the user give correct OTP we can proceed to next page.
