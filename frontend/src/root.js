import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'

import { Navbar, PrivateRoute } from './components'
import Views from './views'

// Note on `PrivateRoute`
//
// From the component src code you can see that you can
// restrict user access based on applications-portal roles
// just add the parameter "roles={['role-name']}" to a private route
// and users without that role will see a permission denied modal and be redirected to home
//
// Example (based on applications-portal-qa), only users in viz-role will load that component:
// <PrivateRoute roles={['viz-role']} component={Views.DataExplorer.Histograms2D} />

const Root = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path='/' element={<Views.Home.Index />} />
        <Route path='/ingest' element={<PrivateRoute component={Views.DataIngestion.Index} />} />
        <Route path='/file-index' element={<PrivateRoute component={Views.DataExplorer.FileIndex} />} />
        <Route path='/runs'>
          <Route index element={<PrivateRoute component={Views.DataExplorer.Runs} />}/>
          <Route path=':runNumber' element={<PrivateRoute component={Views.DataExplorer.Run} />}/>
        </Route>
        <Route path='/lumisections'>
          <Route index element={<PrivateRoute component={Views.DataExplorer.Lumisections} />}/>
          <Route path=':id' element={<PrivateRoute component={Views.DataExplorer.Lumisection} />}/>
        </Route>
        <Route path='/histograms-1d'>
          <Route index element={<PrivateRoute component={Views.DataExplorer.Histograms1D} />}/>
          <Route path=':id' element={<PrivateRoute component={Views.DataExplorer.Histogram} dim={1} />}/>
        </Route>
        <Route path='/histograms-2d'>
          <Route index element={<PrivateRoute component={Views.DataExplorer.Histograms2D} />}/>
          <Route path=':id' element={<PrivateRoute component={Views.DataExplorer.Histogram} dim={2} />}/>
        </Route>
        <Route path='/create' element={<PrivateRoute component={Views.MachineLearning.CreatePipelines} />} />
        <Route path='/train' element={<PrivateRoute component={Views.MachineLearning.RunPipelines} />} />
        <Route path='/predict' element={<PrivateRoute component={Views.MachineLearning.ModelPredict} />} />
      </Routes>
      <ToastContainer
        position='bottom-right'
      />
    </>
  )
}

export default Root
