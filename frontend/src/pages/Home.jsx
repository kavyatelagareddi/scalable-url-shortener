import URLForm from '../components/URLForm'

function Home() {

  return (

    <div className="min-h-screen flex justify-center items-center bg-gray-100">

      <div className="w-[700px] bg-white rounded-3xl shadow-xl p-10">

        <h1 className="text-4xl font-bold mb-3">

          🚀 Scalable URL Shortener

        </h1>

        <p className="text-gray-500 mb-8">

          Create, manage and track your links

        </p>

        <URLForm />

      </div>

    </div>

  )

}

export default Home