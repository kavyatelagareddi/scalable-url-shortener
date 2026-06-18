import { useState } from 'react'

import axios from 'axios'

import ShortURLCard from './ShortURLCard'

function URLForm() {

  const [url, setUrl] = useState('')

  const [alias, setAlias] = useState('')

  const [expiry, setExpiry] = useState('')

  const [result, setResult] = useState(null)

  const generateURL = async () => {

    try {

      const response = await axios.post(

        'http://127.0.0.1:8000/shorten',

        {

          url,

          custom_alias:

          alias || null,

          expiry_days:

          expiry === ''

          ? null

          : Number(expiry)

        }

      )

      setResult(response.data)

    }

    catch (error) {

      alert('Please enter a valid URL')

    }

  }

  return (

    <div>

      <input

        className="w-full p-4 border rounded-xl mb-4"

        placeholder="https://example.com"

        value={url}

        onChange={(e) =>

          setUrl(e.target.value)

        }

      />

      <input

        className="w-full p-4 border rounded-xl mb-4"

        placeholder="Custom Alias"

        value={alias}

        onChange={(e) =>

          setAlias(e.target.value)

        }

      />

      <input

        className="w-full p-4 border rounded-xl mb-6"

        type="number"

        placeholder="Expiry Days"

        value={expiry}

        onChange={(e) =>

          setExpiry(e.target.value)

        }

      />

      <button

        className="w-full bg-blue-600 text-white p-4 rounded-xl"

        onClick={generateURL}

      >

        Generate

      </button>

      {

        result &&

        <ShortURLCard

          data={result}

        />

      }

    </div>

  )

}

export default URLForm