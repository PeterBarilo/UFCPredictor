import { useContext, useState } from 'react';
import FighterContext from './FighterContext';

export default function FighterBox() {
  const [fighter1, setFighter1] = useState('');
  const [fighter2, setFighter2] = useState('');
  const [warning, setWarning] = useState('');
  const { change, setChange, setResult, submitted, setSubmitted } = useContext(FighterContext);


  const handleSubmit = (event) => {
    event.preventDefault();

    if (fighter1.trim() === '' || fighter2.trim() === '') {
      setWarning('Please fill in both fighter names.');
      return;
    }

    setWarning('');

    const value = { fighter1, fighter2 };
    setResult("Performing Ultra Deep Analysis...");
    fetch('/api/retrieve', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(value)
    })
    .then(() => setChange(!change));
    setSubmitted(true)

  };

  return (
    <div className="grid grid-cols-2 gap-6 mx-auto max-w-xl p-6 bg-gray-100 rounded-lg shadow-md font-rubik">
      <div>
        <h4 className="text-gray-600 text-lg font-medium mb-2">FIGHTER 1</h4>
        <input
          type="text"
          id="name1"
          value={fighter1}
          onChange={(event) => setFighter1((event.target.value).toLowerCase())}
          className="w-full py-2 px-3 mb-3 rounded-md border border-gray-300 outline-none"
          placeholder="Input Name"
        />
      </div>

      <div>
        <h4 className="text-gray-600 text-lg font-medium mb-2">FIGHTER 2</h4>
        <input
          type="text"
          id="name2"
          value={fighter2}
          onChange={(event) => setFighter2((event.target.value).toLowerCase())}
          className="w-full py-2 px-3 mb-3 rounded-md border border-gray-300 outline-none"
          placeholder="Input Name"
        />
      </div>

      <div className="col-span-2 flex justify-center">
        <button onClick={handleSubmit} className=" font-rubik bg-ufcred text-black py-2 px-4 rounded-md hover:bg-darkred hover:text-white ease-in duration-300 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-opacity-50">
          Submit
        </button>
      </div>

      {warning && <p className="text-red-500 text-sm mt-2 col-span-2 text-center">{warning}</p>}
    </div>
  );
}
