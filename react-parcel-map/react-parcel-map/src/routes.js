import { Routes, Route } from 'react-router-dom'
import MapPage from './components/get-parcel.component'

const Home = () => <h2>Home</h2>

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path='/' element={<MapPage />} />
    </Routes>
  )
}
