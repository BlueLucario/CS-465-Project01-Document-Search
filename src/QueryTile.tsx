import TextField from '@mui/material/TextField';
import { useState } from 'react';
import SendIcon from '@mui/icons-material/Send';
import Grid from '@mui/material/Grid';
import List from '@mui/material/List';
import { Box, ListItem, ListItemText } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';

export default function QueryTile() {
    const [relevantDocuments, setRelevantDocuments] = useState([]);
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);

    function sendQuery() {
        setLoading(true);

        fetch(`/api/relevantDocuments/${query}`)
        .then(res => res.json())
        .then(data => setRelevantDocuments(data))
        .finally(() => setLoading(false));
    }

    return (
        <>
            <Grid container spacing={1} alignItems="center">
                <Grid item>
                    <TextField style={{width: 350}} id="search-query" label="Search query"
                        variant="outlined" onChange={(e)=>setQuery(e.target.value)} 
                        onKeyDown={(e) => {if(e.key == 'Enter') {sendQuery()}}}/>
                </Grid>
                <Grid item>
                    <LoadingButton id="send-query" onClick={sendQuery} loading={loading}
                    endIcon={<SendIcon/>} loadingPosition="end" variant="contained">
                        <span>Send</span>
                    </LoadingButton>
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
