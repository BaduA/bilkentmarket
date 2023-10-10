import React, { useState } from 'react';
import styled from 'styled-components';

const AutocompleteContainer = styled.div`
  position: relative;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
`;

const OptionsList = styled.ul`
  position: absolute;
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 0 0 5px 5px;
  background-color: #fff;
  z-index: 10;
`;

const OptionItem = styled.li`
  padding: 10px;
  cursor: pointer;

  &:hover {
    background-color: #f0f0f0;
  }
`;

const AutocompleteInput = ({ options, onSelect }) => {
  const [inputValue, setInputValue] = useState('');
  const [showOptions, setShowOptions] = useState(false);

  const handleInputChange = (event) => {
    const value = event.target.value;
    setInputValue(value);
    setShowOptions(value.length > 0);
  };

  const handleOptionClick = (option) => {
    setInputValue(option);
    setShowOptions(false);
    onSelect(option);
  };

  const filteredOptions = options.filter((option) =>
    option.toLowerCase().includes(inputValue.toLowerCase())
  );

  return (
    <AutocompleteContainer>
      <Input
        type="text"
        placeholder="Search..."
        value={inputValue}
        onChange={handleInputChange}
      />
      {showOptions && (
        <OptionsList>
          {filteredOptions.map((option, index) => (
            <OptionItem key={index} onClick={() => handleOptionClick(option)}>
              {option}
            </OptionItem>
          ))}
        </OptionsList>
      )}
    </AutocompleteContainer>
  );
};

export default AutocompleteInput;
