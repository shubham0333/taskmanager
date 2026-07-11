import React from 'react'
import { useNavigate } from 'react-router-dom'


const Navbar = () => {

  const navigate = useNavigate()
  const logout=()=>{
    localStorage.removeItem("token")
    navigate("/")
  }
  return (
    <>
        <div className="navbar">
            <h1>Task Manager</h1>
            <button onClick={logout}>Logout</button>
        </div>
    </>
  )
}

export default Navbar
