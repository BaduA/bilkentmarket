import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import styled from "styled-components";
import AutocompleteInput from "../../CommonComponents/AutocompleteInput";
import "./AddItem.css";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useMutation, useQuery } from "react-query";
import axios from "axios";

const PageContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 20px;
`;

const LeftSection = styled.div`
  width: 50%;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const RightSection = styled.div`
  width: 50%;
  padding: 30px;
`;

const InputContainer = styled.div`
  margin-bottom: 10px;
`;

const InputLabel = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
`;

const InputField = styled.input`
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
`;

const SubmitButton = styled.button`
  padding: 10px 20px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
`;

const options = ["Giyim", "Teknolojik"];

const ImageUploadPage = () => {
  let navigate = useNavigate();
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [description, setDescription] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [categories, setCategories] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    var copyList = selectedFiles;

    if (file) {
      var reader = new FileReader();
      reader.onloadend = function () {
        let isIn = false;
        selectedFiles.forEach((oldfile) => {
          if (oldfile.src === reader.result) {
            console.log("ff");
            isIn = true;
          }
        });
        if (!isIn) {
          copyList.push({
            src: reader.result,
            file: file,
            order: selectedFiles.length + 1,
          });
          setSelectedFiles(copyList);
          setSelectedFile(reader.result);
        }
      };

      reader.readAsDataURL(file);
    } else {
    }
  };
  function getFormData(object) {
    const formData = new FormData();
    for (var key in object) {
      formData.append(key, object[key]);
    }
    return formData;
  }
  const Addfile = useMutation({
    mutationFn: () => {
      var formdata = getFormData({
        description: description,
        name: name,
        price: price,
      });
      selectedFiles.forEach((element) => {
        formdata.append("images", element.file);
      });
      categories.forEach((element) => {
        formdata.append("categorynames", element);
      });
      return axios
        .post("http://127.0.0.1:8000/items/", formdata)
        .then((res) => {});
    },
    onSuccess: () => {
      // navigate("/");
    },
  });
  const handleSubmit = (event) => {
    Addfile.mutate();
    event.preventDefault();
  };
  const handleSelect = (selectedOption) => {
    setSelectedCategory(selectedOption);
    setCategories([...categories, selectedOption]);
  };

  return (
    <PageContainer>
      <LeftSection>
        <h2>Images</h2>
        <div id="itemImg">
          {selectedFile && (
            <>
              {" "}
              <img src={selectedFile} alt="" />
            </>
          )}
        </div>
        <div className="addImage">
          {selectedFiles.length > 0 && (
            <>
              {selectedFiles.map((file) => {
                return (
                  <div
                    className={
                      "littleImage " +
                      (selectedFile === file.src && "activeImg")
                    }
                    onClick={() => {
                      setSelectedFile(file.src);
                    }}
                  >
                    <img src={file.src} alt="" />
                  </div>
                );
              })}
            </>
          )}
          {selectedFiles.length < 3 && (
            <>
              <label htmlFor="file-input">+</label>
              <input
                id="file-input"
                type="file"
                style={{ display: "none" }}
                onChange={handleFileSelect}
              />
            </>
          )}
        </div>
      </LeftSection>
      <RightSection>
        <h2>Image Information</h2>
        <form onSubmit={handleSubmit}>
          <InputContainer>
            <InputLabel>Name:</InputLabel>
            <InputField
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </InputContainer>
          <InputContainer>
            <InputLabel>Price (TL):</InputLabel>
            <InputField
              type="text"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </InputContainer>
          <InputContainer>
            <InputLabel>Description:</InputLabel>
            <InputField
              type="textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </InputContainer>
          <InputContainer>
            <InputLabel>Categories:</InputLabel>
            <AutocompleteInput options={options} onSelect={handleSelect} />
            {categories.length > 0 && (
              <>
                {" "}
                {categories.map((c) => {
                  return (
                    <div className="selectedCategory">
                      {c}
                      <FontAwesomeIcon
                        style={{ marginLeft: "10px", cursor: "pointer" }}
                        icon={faX}
                        onClick={() => {
                          setCategories(categories.filter((cat) => cat !== c));
                        }}
                      ></FontAwesomeIcon>
                    </div>
                  );
                })}
              </>
            )}
          </InputContainer>
          <SubmitButton type="submit">Submit</SubmitButton>
        </form>
      </RightSection>
    </PageContainer>
  );
};

export default ImageUploadPage;
