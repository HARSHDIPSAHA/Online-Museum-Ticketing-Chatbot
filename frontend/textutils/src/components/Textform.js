import React, {useState} from 'react'

export default function Textform(props) {
    const handleUpClick=()=>{
        console.log("Uppercase was clicked" + text);
        let newText=text.toUpperCase();
        setText(newText)
    }
    const handleLoClick=()=>{
      console.log("Lowercase was clicked" + text);
      let newText=text.toLowerCase();
      setText(newText)
  }
  const handleClearClick=()=>{
    console.log("this was clicked" + text);
    let newText=('');
    setText(newText)
}
  const handleCapitalizeClick=()=>{
    console.log("capitalize was clicked" + text);
    const words = text.split(" ");

for (let i = 0; i < words.length; i++) {
    words[i] = words[i][0].toUpperCase() + words[i].substr(1);
}

const newText = words.join(" ");
setText(newText);
}
    const handleOnChange=(event)=>{
        console.log("on change");
        setText(event.target.value)
    }
    const [text, setText] =useState('');

  return (
    <>
    <div className='container'>
        <h1>{props.heading}</h1>
<div className="mb-3">
  <label for="reactbox" className="form-label"></label>
  <textarea className="form-control" value={text} onChange={handleOnChange} id="reactbox" rows="8"></textarea>
</div>
<button className="btn btn-primary mx-2" onClick={handleUpClick}>Convert to Uppercase</button>
<button className="btn btn-primary mx-2" onClick={handleLoClick}>Convert to Lowercase</button>
<button className="btn btn-primary mx-2" onClick={handleClearClick}>Clear Text</button>
<button className="btn btn-primary mx-2" onClick={handleCapitalizeClick}>Capitalize all Text</button>
    </div>
    <div className="container my-3">
        <h1>Your text summary</h1>
        <p>{text.split(" ").length} and {text.length} characters</p>
        <p>{0.008 * text.split(" ").length} Minutes read</p>
        <h2>Preview</h2>
        <p>{text}</p>
       </div>
    </>
  )
}
//hooks let you use class features without actually making a class
//very useful in function based components
