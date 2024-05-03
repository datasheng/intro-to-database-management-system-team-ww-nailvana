const SignUp = () => {
    
    return (
        <div className="signup">
            <h2>Sign up Here:</h2>
            <form>
                <label>Name:</label>
                <input 
                    type="text"
                    id="customerName"
                    required                
                />

                <label>Email:</label>
                <input 
                    type="email" 
                    id="customerEmail"
                    size="30"                 
                />

                <label>Username:</label>
                <input 
                    type="text"
                    id="customerUsername"
                    maxLength={8}
                    required                
                />

                <label>Password:</label>
                <input 
                    type="password"
                    id="customerPassword"
                    maxLength={20}
                    required                
                />
                
                <label>Phone Number:</label>
                <input 
                    type="tel"
                    id="customerPhoneNumber"
                    pattern="[0-9]{10}"
                    maxLength={10}
                    required
                />

                <label>Address:</label>
                <input 
                    type="text"
                    id="customerAddress"
                    maxLength={30}
                    required                
                />

                <button>Sign Up</button>
            </form>
        </div>
    );
}
 
export default SignUp;