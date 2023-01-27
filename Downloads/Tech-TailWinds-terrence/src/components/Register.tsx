import React, { useState } from 'react'
import { SocialIcon } from 'react-social-icons'

type Props = {}

const Register = (props: Props) => {
    const [usrName, setUsername] = useState();
    const [email, setEmail] = useState();
    const [pass, setPass] = useState();
    return (
        <div className='auth-form-container'>
            <p style={{fontWeight:'bolder'}}>SignUp</p>
            <form className='register-form'>
                <label htmlFor='username'>Username</label>
                <input placeholder="username" id="username" name="email" value={usrName} />
                <label htmlFor='email'>Email</label>
                <input type="email" placeholder="youremail@xyz.com" id="email" name="email" value={email} />
                <label htmlFor='password'>Password</label>
                <input type="password" placeholder="password" id="password" name="password" value={pass} />
                <button className='register-btn'>Register</button>
            </form>
            <div>
                <p className='or'>OR</p>
                <div style={{ paddingTop: 15 }}>
                    <SocialIcon network="google" bgColor="#db4437" style={{ height: 25, width: 25 }} />
                    <SocialIcon network="facebook" bgColor="#3b5998" style={{ height: 25, width: 25 }} />
                    <SocialIcon network="linkedin" bgColor="#0072b1" style={{ height: 25, width: 25 }} />
                </div>
                <button className='link-btn' >Already a user? <span>Login</span></button>
            </div>

        </div>
    )
}

export default Register