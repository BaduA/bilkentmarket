import React, { useState } from 'react';
import styled from 'styled-components';

const CustomSelectContainer = styled.div`
  position: relative;
  display: inline-block;
`;

const CustomSelectButton = styled.button`
  padding: 12px 24px;
  border: 2px solid #3498db;
  border-radius: 8px;
  background-color: #f9f9f9;
  color: #333;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;

  &:hover {
    background-color: #e0e0e0;
  }
`;

const OptionsContainer = styled.div`
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  border: 2px solid #3498db;
  border-radius: 0 0 8px 8px;
  background-color: #f9f9f9;
  max-height: 150px;
  overflow-y: auto;
`;

const Option = styled.div`
  padding: 12px 24px;
  cursor: pointer;

  &:hover {
    background-color: #e0e0e0;
  }
`;

const CustomSelect = ({ options, value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleOptionClick = optionValue => {
    onChange(optionValue);
    setIsOpen(false);
  };

  return (
    <CustomSelectContainer>
      <CustomSelectButton onClick={() => setIsOpen(!isOpen)}>
        {options.find(option => option.value === value)?.label || 'Select an option'}
      </CustomSelectButton>
      {isOpen && (
        <OptionsContainer>
          {options.map(option => (
            <Option
              key={option.value}
              onClick={() => handleOptionClick(option.value)}
            >
              {option.label}
            </Option>
          ))}
        </OptionsContainer>
      )}
    </CustomSelectContainer>
  );
};

export default CustomSelect;
