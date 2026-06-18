import { useState } from 'react'

import axios from 'axios'

function ShortURLCard({ data }) {

  const [analytics, setAnalytics] = useState(null)

  const copyURL = () => {

    navigator.clipboard.writeText(

      data.short_url

    )

    alert('Copied!')

  }

  const getAnalytics = async () => {

    const shortCode =

      data.short_url

      .split('/')

      .pop()

    const response = await axios.get(

      `http://127.0.0.1:8000/analytics/${shortCode}`

    )

    setAnalytics(

      response.data

    )

  }

  return (

    <div className="mt-8 p-6 bg-gray-100 rounded-2xl">

      <h3 className="text-2xl font-bold mb-3">

        Generated URL

      </h3>

      <p className="mb-5">

        {data.short_url}

      </p>

      <div className="flex gap-4">

        <button

          className="bg-green-600 text-white px-5 py-3 rounded-xl"

          onClick={copyURL}

        >

          📋 Copy

        </button>

        <button

          className="bg-purple-600 text-white px-5 py-3 rounded-xl"

          onClick={getAnalytics}

        >

          📊 Analytics

        </button>

      </div>

      {

        analytics &&

        <div className="mt-6">

          <p>

            <strong>Clicks:</strong>

            {' '}

            {analytics.clicks}

          </p>

          <p>

            <strong>Created:</strong>

            {' '}

            {analytics.created_at}

          </p>

          <p>

            <strong>Expires:</strong>

            {' '}

            {analytics.expires_at || 'Never'}

          </p>

        </div>

      }

    </div>

  )

}

export default ShortURLCard