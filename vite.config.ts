// vite.config.ts (typescript)
// Will Moss & Benjamin Weeg (Group 1)
// Started: 
// Last edited: 2024-05-09 (yyyy mm dd)

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            "^/api/.": {
                target: "http://localhost:5000",
                changeOrigin: true,
                secure: false,
                ws: true,
            }
        },
        watch: {
            usePolling: true,
        },
    },
})
