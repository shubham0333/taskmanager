import React, { useState } from 'react'
import { ENDPOINTS, instance } from './api'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'

const Login = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [isRegister, setIsRegister] = useState(false)
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)

        try {
            const endpoint = isRegister ? ENDPOINTS.REGISTER() : ENDPOINTS.LOGIN()
            const response = await instance.post(
                endpoint,
                { username: username.trim(), password },
                { skipAuthRedirect: true },
            )

            if (isRegister) {
                toast.success('Registration successful. Please login now.')
                setIsRegister(false)
                setPassword('')
            } else {
                if (!response.data?.access_token) {
                    throw new Error('The server did not return an access token.')
                }
                localStorage.setItem('token', response.data.access_token)
                toast.success('Login successful')
                navigate('/tasks')
            }
        } catch (err) {
            const message = err?.response?.data?.detail || err?.message || 'Request failed'
            toast.error(message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className='container'>
            <form onSubmit={handleSubmit} className='login-form'>
                <div className='auth-toggle'>
                    <button
                        type='button'
                        className={!isRegister ? 'active' : ''}
                        onClick={() => setIsRegister(false)}
                    >
                        Login
                    </button>
                    <button
                        type='button'
                        className={isRegister ? 'active' : ''}
                        onClick={() => setIsRegister(true)}
                    >
                        Register
                    </button>
                </div>

                <h2>{isRegister ? 'Register' : 'Login'}</h2>

                <input
                    type='text'
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder='Username'
                    required
                />
                <input
                    type='password'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder='Password'
                    required
                />

                <button type='submit' disabled={loading}>
                    {loading ? 'Please wait...' : isRegister ? 'Register' : 'Login'}
                </button>
            </form>
        </div>
    )
}

export default Login
