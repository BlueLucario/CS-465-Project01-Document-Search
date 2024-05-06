import TextField from '@mui/material/TextField';
import { useState } from 'react';
import SendIcon from '@mui/icons-material/Send';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import { AlertColor, Box, ListItem, ListItemText } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
import UploadIcon from './UploadIcon';

export default function QueryTile(props: { showSnackbar: (severity: AlertColor, message: string) => void; }) {
    const [relevantDocuments, setRelevantDocuments] = useState([]);
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);

    function sendQuery() {
        setLoading(true);

        fetch(`/api/relevantDocuments/${query.toString().toLowerCase()}`)
                .then(res => {
                    if (!res.ok) {
                        const error = new Error(res.statusText);
                        console.log(error);
                        error.response = res;
                        error.status = res.status;
                        throw error;
                    }
                    return res.json()
                })
                .then(data => setRelevantDocuments((data.length == 0) ? ['No documents found'] : data))
                .catch((err) => {
                    err.response.text().then((data: string) => {
                        const message = (data.trim() != '') ? `Error: ${data}` : `${err}`;
                        const severity = "error";
                        props.showSnackbar(severity, message);
                    })
                })
                .finally(() => setLoading(false));
    }

    return (
        <>
            <Grid container spacing={1} alignItems="center">
                {loading ? <span>Loading...</span> : null}
                <Grid item>
                    <TextField style={{width: 350}} id="search-query" label="Search query"
                            variant="outlined" onChange={(e)=>setQuery(e.target.value)} 
                            onKeyDown={(e) => {if (e.key == 'Enter') {sendQuery()}}}/>
                </Grid>
                <Grid item>
                    <LoadingButton id="send-query" onClick={sendQuery} loading={loading}
                            endIcon={<SendIcon/>} loadingPosition="end" variant="contained">
                        <span>Send</span>
                    </LoadingButton>
                </Grid>
                <Grid item>
                    <UploadIcon showSnackbar={props.showSnackbar} />
                </Grid>
            </Grid> 

            <p>Relevant documents:</p>
            <Box sx={{maxHeight: '300px', overflow: 'auto'}}>

                <span>{relevantDocuments.map(document => 
                    <List key={`list-${document}`}>
                        <ListItem key={`listItem-${document}`}>
                            <ListItemText key={`listItemText-${document}`} primary={document} />
                        </ListItem>
                    </List>
                )}</span>
            </Box>
        </>
    );
}
