import TextField from '@mui/material/TextField';
import { useState } from 'react';
import SendIcon from '@mui/icons-material/Send';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';

export default function QueryTile() {
    const [relevantDocuments, setRelevantDocuments] = useState([]);
    const [query, setQuery] = useState('');

    function sendQuery() {
        fetch(`/api/getRelevantDocuments/${query}`)
        .then(res => res.json()).then(data => {
            setRelevantDocuments(data)
        });
    }

    return (
        <>
            <Grid container alignItems="center">
                <Grid item>
                    <TextField style={{width: 350}} id="search-query" label="Search query"
                        variant="outlined" onChange={(e)=>setQuery(e.target.value)} 
                        onKeyDown={(e) => {if(e.key == 'Enter') {sendQuery()}}}/>
                </Grid>
                <Grid item>
                    <IconButton id="send-query" onClick={sendQuery}><SendIcon/></IconButton>
                </Grid>
            </Grid> 

            <p>The relevant documents are {relevantDocuments.map(document => 
                <li key={document}>{document}</li>
            )}</p>
        </>
    );
}
