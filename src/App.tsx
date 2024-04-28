import './App.css'
import './QueryTile'
import QueryTile from './QueryTile'
import Grid from '@mui/material/Grid';
import DownloadStats from './DownloadStats';

function App() {
	return (
		<>
			<Grid container direction="column" spacing={2}>
				<Grid item>
					<h1>Document Retrieval</h1>
				</Grid>
				<Grid item>
					<QueryTile />
				</Grid>
			</Grid>

			<div style={{ position: "absolute", bottom: 10, right: 10, zIndex: 999 }}>
				<DownloadStats/>
			</div>
		</>
	)
}

export default App
