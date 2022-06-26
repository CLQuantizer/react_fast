import { 
  ChakraProvider,
  Button,
  Box,
  Link,
  Grid,
  GridItem,
  theme,
} from '@chakra-ui/react';
import React, { StrictMode } from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Journals from './Journals'
import {BrowserRouter,Routes,Route,} from "react-router-dom";
import { ColorModeSwitcher } from './ColorModeSwitcher';

// development server
const devlopment_addr = 'http://localhost:3000/';
// production server
const production_addr = 'http://langedev.net/';

const addr = devlopment_addr;

ReactDOM.render(
  <StrictMode>
  <ChakraProvider theme={theme}>
  <Box textAlign="center" fontSize="xl">
    <Grid minH="5vh" p={3}>
      <ColorModeSwitcher justifySelf="flex-end" />
    </Grid>

    <Grid templateColumns='repeat(3, 1fr)' gap={6}>
      <GridItem w='100%' h='10' >
        <Button variant = 'outline'>
          <Link href ={addr}>Home</Link>
        </Button>
      </GridItem>

      <GridItem w='100%' h='10'>
        <Button variant = 'outline'>
          <Link href = {addr +'journals/'}>Journals</Link>
        </Button>
      </GridItem>

      <GridItem w='100%' h='10'>
        <Button variant = 'outline'>
          <Link href = 'https://google.co.uk'>Google</Link>
        </Button>
      </GridItem>

    </Grid>
  </Box>
  <br/>
  
    <BrowserRouter>
    <Routes>
      <Route path = "/" element={<App/>}/>
      <Route path = "/journals/" element={<Journals/>}/>
    </Routes>
    </BrowserRouter>
    </ChakraProvider>
  </StrictMode>,
	document.getElementById('root') 
);

