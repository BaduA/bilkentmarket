import React from 'react'
import "./Commons.css"

function Message({message,fontsize}) {
  return (
    <div className='messageContainer' style={{fontSize:fontsize}}>{message}</div>
  )
}

export default Message