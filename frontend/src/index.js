import { 
  ColorModeScript,
  ChakraProvider,
  Button,
  Box,
  Text,
  Link,
  VStack,
  Input,
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

ReactDOM.render(
  <StrictMode>
  <ChakraProvider theme={theme}>
  <Box textAlign="center" fontSize="xl">
    <Grid minH="5vh" p={3}>
      <ColorModeSwitcher justifySelf="flex-end" />
    </Grid>

    <Grid templateColumns='repeat(3, 1fr)' gap={6}>
      <GridItem w='100%' h='10' bg='teal'>
        <Link theme={theme} href = 'http://localhost:3000/'>Home</Link>
      </GridItem>

      <GridItem w='100%' h='10' bg='teal'>
        <Link theme={theme} href = 'http://localhost:3000/journals/'>Journals</Link>
      </GridItem>

      <GridItem w='100%' h='10' bg='teal'>
        <Link theme={theme}  href = 'https://google.co.uk'>Google</Link>
      </GridItem>

    </Grid>
  </Box>

  
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

