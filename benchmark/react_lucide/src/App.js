import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  ArrowRight, 
  ArrowLeft, 
  Download, 
  RefreshCw, 
  CheckCircle,
  AlertCircle,
  FileText,
  ChevronRight
} from 'lucide-react';
import './App.css';

import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Progress } from "./components/ui/progress";
import { Textarea } from "./components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Badge } from "./components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert";
import { ScrollArea } from "./components/ui/scroll-area";

const App = () => {
  // State for managing the multi-step form
  const [currentStep, setCurrentStep] = useState(1);
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescriptionFile, setJobDescriptionFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [resumeContent, setResumeContent] = useState('');
  const [isDraggingResume, setIsDraggingResume] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [matchScore, setMatchScore] = useState(0);
  const [finalMatchScore, setFinalMatchScore] = useState(0);
  const [matchedSkills, setMatchedSkills] = useState([]);
  const [missingSkills, setMissingSkills] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [selectedFormat, setSelectedFormat] = useState('pdf');
  const [optimizedContent, setOptimizedContent] = useState('');

  // Function to handle resume file drop
  const handleResumeDrop = (event) => {
    event.preventDefault();
    setIsDraggingResume(false);
    if (event.dataTransfer.files.length > 0) {
      setResumeFile(event.dataTransfer.files[0]);
      readResumeFile(event.dataTransfer.files[0]);
    }
  };

  // Function to handle resume file selection
  const handleResumeSelect = (event) => {
    if (event.target.files.length > 0) {
      setResumeFile(event.target.files[0]);
      readResumeFile(event.target.files[0]);
    }
  };

  // Function to read resume file content
  const readResumeFile = (file) => {
    // In real implementation, this would parse the file
    // For demo purposes, we'll just set mock content
    setResumeContent("<p><strong>John Doe</strong><br>Software Engineer<br>john.doe@email.com</p><p><strong>Experience</strong><br>Senior Developer, ABC Tech (2020-Present)<br>- Developed web applications using React and Node.js<br>- Implemented CI/CD pipelines</p><p><strong>Skills</strong><br>JavaScript, React, Node.js, Git, Agile</p><p><strong>Education</strong><br>BS Computer Science, University of Technology (2016-2020)</p>");
  };

  // Function to handle job description file selection
  const handleJobDescriptionSelect = (event) => {
    if (event.target.files.length > 0) {
      setJobDescriptionFile(event.target.files[0]);
      // In real implementation, this would parse the file
      setJobDescription("We are looking for a skilled Software Engineer with experience in React, Node.js, and Python. The ideal candidate should have knowledge of AWS, CI/CD, and Docker. Experience with TypeScript and GraphQL is preferred.");
    }
  };

  // Function to check if we can proceed to analysis
  const canProceedToAnalysis = () => {
    return (resumeFile && resumeContent) && 
           (jobDescription || jobDescriptionFile);
  };

  // Function to analyze resume
  const analyzeResume = () => {
    if (!canProceedToAnalysis()) return;
    
    setCurrentStep(2);
    setIsAnalyzing(true);
    
    // In a real implementation, this would be an API call to your FastAPI backend
    // For demo purposes, we'll simulate API response with a timeout
    setTimeout(() => {
      setIsAnalyzing(false);
      setMatchScore(65);
      setMatchedSkills(["JavaScript", "React", "Node.js"]);
      setMissingSkills(["Python", "AWS", "Docker", "TypeScript", "GraphQL"]);
      
      // Reset suggestions each time we analyze
      setSuggestions([
        {
          id: 1,
          title: "Add Python experience",
          description: "The job requires Python but it's not mentioned in your resume. If you have experience with Python, add it to your skills section."
        },
        {
          id: 2,
          title: "Highlight AWS experience",
          description: "AWS knowledge is required. Include any AWS experience you have or mention relevant cloud experience."
        },
        {
          id: 3,
          title: "Add Docker to your skills",
          description: "Docker experience is required. If you have containerization experience, add it to your skills section."
        }
      ]);
    }, 2000);
  };

  useEffect(() => {
    if (currentStep === 3) {
      // In real implementation, this would be an API call
      // For demo purposes, we'll set mock content after a short delay
      setTimeout(() => {
        setOptimizedContent(`
          <p><strong>John Doe</strong><br>Software Engineer<br>john.doe@email.com</p>
          <p><strong>Experience</strong><br>Senior Developer, ABC Tech (2020-Present)<br>
          - Developed scalable web applications using React and Node.js<br>
          - Implemented CI/CD pipelines for automated testing and deployment<br>
          - Collaborated with cross-functional teams on AWS-based solutions</p>
          <p><strong>Skills</strong><br>
          JavaScript, React, Node.js, Git, Agile, Python, AWS, Docker</p>
          <p><strong>Education</strong><br>BS Computer Science, University of Technology (2016-2020)</p>
        `);
        console.log('Current suggestions:', suggestions);
        // Make sure we have suggestions in case they were cleared
        if (suggestions.length === 0) {
          setSuggestions([
            {
              id: 1,
              title: "Add Python experience",
              description: "The job requires Python but it's not mentioned in your resume. If you have experience with Python, add it to your skills section."
            },
            {
              id: 2,
              title: "Highlight AWS experience",
              description: "AWS knowledge is required. Include any AWS experience you have or mention relevant cloud experience."
            },
            {
              id: 3,
              title: "Add Docker to your skills",
              description: "Docker experience is required. If you have containerization experience, add it to your skills section."
            }
          ]);
        }
      }, 1000);
    }
  }, [currentStep, suggestions.length]);

  // Function to accept a suggestion
  const acceptSuggestion = (id) => {
    // Remove the suggestion from the list
    setSuggestions(suggestions.filter(suggestion => suggestion.id !== id));
    // Update match score
    const newScore = matchScore + 5;
    setMatchScore(newScore);
    // Update final match score - must be based on the new score
    setFinalMatchScore(newScore + 15);
  };

  // Function to download resume
  const downloadResume = () => {
    // In real implementation, this would make an API call and trigger a download
    // For demo purposes, we'll just log the request
    console.log(`Downloading resume in ${selectedFormat} format`);
    
    // You would make an API call here
    // axios.post('/api/download-resume', { format: selectedFormat })
    //   .then(response => {
    //     // Handle file download
    //   });
  };

  // Function to start over
  const startOver = () => {
    setCurrentStep(1);
    setResumeFile(null);
    setJobDescriptionFile(null);
    setJobDescription('');
    setResumeContent('');
    setMatchScore(0);
    setFinalMatchScore(0);
    setMatchedSkills([]);
    setMissingSkills([]);
    setSuggestions([]);
    setSelectedFormat('pdf');
    setOptimizedContent('');
  };

  // Steps for the progress stepper
  const steps = [
    { number: 1, name: "Upload" },
    { number: 2, name: "Analysis" },
    { number: 3, name: "Optimize" },
    { number: 4, name: "Download" }
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-slate-900">MyResumo</h1>
            <div className="text-sm text-slate-500">Resume Optimization Tool</div>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Resume Optimization</CardTitle>
            <CardDescription>Get your resume ready for the job application process</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Progress Stepper */}
            <div className="relative mb-10">
              <div className="flex items-center justify-between">
                {steps.map((step) => (
                  <div key={step.number} className="flex flex-col items-center">
                    <div 
                      className={`h-10 w-10 rounded-full flex items-center justify-center ${
                        currentStep >= step.number 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-slate-200 text-slate-600'
                      }`}
                    >
                      {step.number}
                    </div>
                    <span className="mt-2 text-sm font-medium">{step.name}</span>
                  </div>
                ))}
              </div>
              <div className="absolute top-5 left-0 right-0 h-0.5 bg-slate-200 -z-10">
                <div 
                  className="h-full bg-blue-600 transition-all duration-500" 
                  style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
                ></div>
              </div>
            </div>

            {/* Step 1: Upload */}
            {currentStep === 1 && (
              <div className="space-y-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Resume Upload */}
                  <Card className="border-dashed">
                    <CardContent className="p-6">
                      <div 
                        className={`h-64 border-2 border-dashed rounded-lg flex flex-col items-center justify-center p-6 transition-colors ${
                          isDraggingResume ? 'border-blue-500 bg-blue-50' : 'border-slate-300 hover:bg-slate-50'
                        }`}
                        onDragOver={(e) => { e.preventDefault(); setIsDraggingResume(true); }}
                        onDragLeave={(e) => { e.preventDefault(); setIsDraggingResume(false); }}
                        onDrop={handleResumeDrop}
                      >
                        <Upload className="h-10 w-10 text-slate-400" />
                        <div className="mt-4 text-center">
                          <h3 className="text-lg font-medium text-slate-900">Upload your resume</h3>
                          <p className="text-sm text-slate-500 mt-1">PDF or DOCX (max 5MB)</p>
                          <div className="mt-4">
                            <label 
                              htmlFor="resume-upload" 
                              className="inline-block"
                            >
                              <div className="inline-flex h-10 items-center justify-center rounded-md bg-white px-4 py-2 text-sm font-medium text-slate-900 ring-1 ring-inset ring-slate-300 hover:bg-slate-50 cursor-pointer">
                                Browse files
                              </div>
                              <input 
                                id="resume-upload" 
                                type="file" 
                                className="hidden" 
                                accept=".pdf,.docx"
                                onChange={handleResumeSelect} 
                              />
                            </label>
                          </div>
                        </div>
                      </div>
                      {resumeFile && (
                        <div className="mt-4 flex items-center p-3 bg-blue-50 rounded-md">
                          <FileText className="h-4 w-4 text-blue-600 mr-2" />
                          <span className="text-sm font-medium">{resumeFile.name}</span>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="ml-auto text-red-500 h-8"
                            onClick={() => setResumeFile(null)}
                          >
                            Remove
                          </Button>
                        </div>
                      )}
                    </CardContent>
                  </Card>

                  {/* Job Description Upload */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Job Description</CardTitle>
                      <CardDescription>Paste the job description or upload a file</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Textarea 
                        className="min-h-40 mb-4" 
                        placeholder="Paste the job description here..."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                      />
                      <div className="flex items-center">
                        <span className="text-sm text-slate-500">Or upload a job posting file</span>
                        <label htmlFor="job-desc-upload" className="ml-4 inline-block">
                          <div className="inline-flex h-9 items-center justify-center rounded-md bg-white px-3 py-2 text-sm font-medium text-slate-900 ring-1 ring-inset ring-slate-300 hover:bg-slate-50 cursor-pointer">
                            Upload file
                          </div>
                          <input 
                            id="job-desc-upload" 
                            type="file" 
                            className="hidden" 
                            accept=".pdf,.docx,.txt"
                            onChange={handleJobDescriptionSelect} 
                          />
                        </label>
                      </div>
                      
                      {jobDescriptionFile && (
                        <div className="mt-4 flex items-center p-3 bg-blue-50 rounded-md">
                          <FileText className="h-4 w-4 text-blue-600 mr-2" />
                          <span className="text-sm font-medium">{jobDescriptionFile.name}</span>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="ml-auto text-red-500 h-8"
                            onClick={() => setJobDescriptionFile(null)}
                          >
                            Remove
                          </Button>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>

                <div className="flex justify-end">
                  <Button 
                    onClick={analyzeResume}
                    disabled={!canProceedToAnalysis()}
                  >
                    Analyze Resume
                    <ChevronRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}

            {/* Step 2: Analysis */}
            {currentStep === 2 && (
              <div className="space-y-8">
                {isAnalyzing ? (
                  <div className="flex flex-col items-center justify-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
                    <p className="mt-4 text-lg font-medium text-slate-900">Analyzing your resume...</p>
                    <p className="text-sm text-slate-500">This may take a few moments</p>
                  </div>
                ) : (
                  <div className="space-y-8">
                    {/* Analysis Results */}
                    <Card>
                      <CardHeader>
                        <CardTitle>Resume Analysis Results</CardTitle>
                        <CardDescription>How well your resume matches this job</CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-6">
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-sm font-medium text-slate-700">ATS Match Score</span>
                            <span className="text-sm font-medium text-slate-700">{matchScore}%</span>
                          </div>
                          <Progress value={matchScore} className="h-2" />
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="text-sm font-medium text-slate-900 mb-3">Key Requirements Found</h4>
                            <div className="flex flex-wrap gap-2">
                              {matchedSkills.map((skill) => (
                                <Badge key={skill} variant="outline" className="bg-green-50 text-green-700 border-green-200">
                                  <CheckCircle className="mr-1 h-3 w-3" />
                                  {skill}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="text-sm font-medium text-slate-900 mb-3">Missing Requirements</h4>
                            <div className="flex flex-wrap gap-2">
                              {missingSkills.map((skill) => (
                                <Badge key={skill} variant="outline" className="bg-red-50 text-red-700 border-red-200">
                                  <AlertCircle className="mr-1 h-3 w-3" />
                                  {skill}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <div className="flex justify-between">
                      <Button 
                        variant="outline"
                        onClick={() => setCurrentStep(1)}
                      >
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back
                      </Button>
                      <Button 
                        onClick={() => setCurrentStep(3)}
                      >
                        Optimize Resume
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Step 3: Optimize */}
            {currentStep === 3 && (
              <div className="space-y-8">
                <Tabs defaultValue="comparison" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="comparison">Resume Comparison</TabsTrigger>
                    <TabsTrigger value="suggestions">Improvement Suggestions</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="comparison" className="mt-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {/* Original Resume */}
                      <Card>
                        <CardHeader>
                          <CardTitle>Original Resume</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ScrollArea className="h-80 w-full rounded-md border p-4">
                            <div dangerouslySetInnerHTML={{ __html: resumeContent }}></div>
                          </ScrollArea>
                        </CardContent>
                      </Card>
                      
                      {/* Optimized Resume */}
                      <Card>
                        <CardHeader>
                          <CardTitle>Optimized Resume</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ScrollArea className="h-80 w-full rounded-md border p-4">
                            {optimizedContent ? (
                              <div dangerouslySetInnerHTML={{ __html: optimizedContent }}></div>
                            ) : (
                              <div className="flex justify-center items-center h-full">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-700"></div>
                              </div>
                            )}
                          </ScrollArea>
                        </CardContent>
                      </Card>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="suggestions" className="mt-6">
                      <Card>
                        <CardHeader>
                          <CardTitle>Improvement Suggestions</CardTitle>
                          <CardDescription>Apply these changes to improve your resume</CardDescription>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-4">
                            {suggestions && suggestions.length > 0 ? (
                              suggestions.map((suggestion) => (
                                <Alert key={suggestion.id} variant="default" className="bg-amber-50 border-amber-200">
                                  <AlertCircle className="h-4 w-4 text-amber-500" />
                                  <AlertTitle>{suggestion.title}</AlertTitle>
                                  <AlertDescription className="mt-1">{suggestion.description}</AlertDescription>
                                  <Button 
                                    variant="outline" 
                                    size="sm" 
                                    className="mt-2 bg-amber-100 text-amber-800 border-amber-200 hover:bg-amber-200 hover:text-amber-900"
                                    onClick={() => acceptSuggestion(suggestion.id)}
                                  >
                                    Apply suggestion
                                  </Button>
                                </Alert>
                              ))
                            ) : (
                              <div className="flex flex-col items-center justify-center py-8 text-center">
                                <CheckCircle className="h-12 w-12 text-green-500 mb-2" />
                                <p className="text-slate-600">All suggestions have been applied!</p>
                              </div>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    </TabsContent>
                </Tabs>

                <div className="flex justify-between">
                  <Button 
                    variant="outline"
                    onClick={() => setCurrentStep(2)}
                  >
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back
                  </Button>
                  <Button 
                    onClick={() => {
                      setFinalMatchScore(matchScore + 15);
                      setCurrentStep(4);
                    }}
                  >
                    Continue
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}

            {/* Step 4: Download */}
            {currentStep === 4 && (
              <div className="space-y-8">
                <div className="max-w-2xl mx-auto">
                  <Card>
                    <CardHeader className="text-center">
                      <CardTitle>Download Your Optimized Resume</CardTitle>
                      <CardDescription>Your resume is ready to be downloaded</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div>
                        <div className="flex justify-between mb-2">
                          <span className="text-sm font-medium text-slate-700">Final ATS Match Score</span>
                          <span className="text-sm font-medium text-slate-700">{finalMatchScore}%</span>
                        </div>
                        <Progress value={finalMatchScore} className="h-2" />
                      </div>
                      
                      <div className="flex flex-col items-center space-y-6">
                        <div className="bg-slate-50 p-6 rounded-lg w-full">
                          <h4 className="text-sm font-medium text-slate-900 mb-4">Choose Format</h4>
                          <div className="flex justify-center space-x-4">
                            {['pdf', 'docx', 'txt'].map((format) => (
                              <Button 
                                key={format}
                                variant={selectedFormat === format ? "default" : "outline"}
                                onClick={() => setSelectedFormat(format)}
                                className="w-24"
                              >
                                {format.toUpperCase()}
                              </Button>
                            ))}
                          </div>
                        </div>
                        
                        <Button 
                          size="lg" 
                          className="w-full sm:w-auto"
                          onClick={downloadResume}
                        >
                          <Download className="mr-2 h-5 w-5" />
                          Download Resume
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <div className="flex justify-between">
                  <Button 
                    variant="outline"
                    onClick={() => setCurrentStep(3)}
                  >
                    <ArrowLeft className="mr-2 h-4 w-4" />
                    Back
                  </Button>
                  <Button 
                    variant="outline"
                    onClick={startOver}
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Start Over
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
      
      <footer className="bg-white border-t border-slate-200 mt-12">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-slate-500 text-sm">
            &copy; 2025 MyResumo. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;