import './App.css'
import './QueryTile'
import QueryTile from './QueryTile'
import UploadTile from './UploadTile'
import Grid from '@mui/material/Grid';

function App() {
  return (
    <>
      <Grid container direction="column" spacing={2}>
        <Grid item>
          <UploadTile />
        </Grid>
        <Grid item>
          <QueryTile />
        </Grid>
      </Grid>
    </>
  )
}

export default App
