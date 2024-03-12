import './App.css';
import Navbar from "./Nav"
import FighterGrid from "./FighterBox"
import React, {useState, useEffect, useContext} from 'react'
import FighterContext from './FighterContext';
function App() {
  const [result, setResult] = useState("")
  const [change, setChange] = useState(false)
  const [fighterA, setFighterA] = useState("")
  const [fighterB, setFighterB] = useState("")
  const [other, setOther] = useState("")
  const [submitted, setSubmitted] = useState(false)
  const [winnerName, setWinnerName] = useState("")

  useEffect(() => {
      console.log("useEffect called")
      fetch("/api/test")
      .then(res => res.json())
      .then(
        data => {
          setResult(data.name)
          setFighterA(data.a)
          setFighterB(data.b)
          setOther(data.other)
          setWinnerName(data.winner)
          console.log(winnerName)
        })
      console.log("fetch complete")
  }, [change])

  return (
    <div className="App text-center	">
  <FighterContext.Provider value={{ change, setChange, result, setResult, submitted, setSubmitted }}>
      <div>
        <Navbar />
      </div>
      <div className='mt-10 mb-5'>
        <h1 className='font-rubik text-4xl mb-5'>UFC FIGHT PREDICTOR</h1>
        <h6 className='font-rubik text-base'>Pick Two Fighters and See How they Match Up</h6>
    </div>
    <div className='mb-5'>
      <FighterGrid />
    </div>
    <p className='font-rubik mb-3'><strong className='font-bold'>WINNER: </strong>{result} </p>
    {submitted===false ? <p></p>:
    <div>
      <p className='font-rubik'>{winnerName}'s chance of winning: <strong>{fighterA}%</strong></p>
      <p className='font-rubik'>{other}'s chance of winning: <strong>{fighterB}%</strong></p>
    </div>
    }
    </FighterContext.Provider>
    </div>
    );
}

export default App;
