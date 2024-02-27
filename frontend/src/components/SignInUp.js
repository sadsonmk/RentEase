import React, { useState } from 'react';

function SignInUp() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSignIn = () => {
        // Handle sign in
        console.log(`Signed in as ${username}`);
    };

    const handleSignUp = () => {
        // Handle sign up
        console.log(`Signed up as ${username}`);
    };

    return (
        <div>
            <h2>Sign In/Up</h2>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleSignIn}>Sign In</button>
            <button onClick={handleSignUp}>Sign Up</button>
        </div>
    );
}

export default SignInUp;