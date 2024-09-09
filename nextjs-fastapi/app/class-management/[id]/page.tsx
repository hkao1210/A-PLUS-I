import React from 'react';
import { Plus, Upload, Clock } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

// Mock data for demonstration purposes
const classDetails = {
  name: "Introduction to Computer Science",
  schedule: "MWF 10:00 AM - 11:30 AM",
  students: 45
};

const tests = [
  { id: 1, name: "Midterm Exam", date: "2024-10-15", status: "Completed" },
  { id: 2, name: "Final Project", date: "2024-12-01", status: "Upcoming" },
  { id: 3, name: "Quiz 3", date: "2024-11-05", status: "Grading" },
];

const students = [
  { id: 1, name: "Alice Johnson", submission: "Submitted", gradingStatus: "Completed" },
  { id: 2, name: "Bob Smith", submission: "Submitted", gradingStatus: "Pending" },
  { id: 3, name: "Charlie Brown", submission: "Not Submitted", gradingStatus: "N/A" },
];

const ClassManagementPage = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Class Management</h1>
      
      {/* Class Details */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Class Details</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-xl font-semibold">{classDetails.name}</p>
          <p className="text-gray-600">Schedule: {classDetails.schedule}</p>
          <p className="text-gray-600">Number of Students: {classDetails.students}</p>
        </CardContent>
      </Card>
      
      {/* Tests Section */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            Tests
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Add New Test
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Test Name</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tests.map((test) => (
                <TableRow key={test.id}>
                  <TableCell>{test.name}</TableCell>
                  <TableCell>{test.date}</TableCell>
                  <TableCell>
                    <Badge variant={test.status === 'Completed' ? 'default' : 'secondary'}>
                      {test.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">View</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
      
      {/* Student Submissions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            Student Submissions
            <Button>
              <Upload className="mr-2 h-4 w-4" /> Upload All Submissions
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Student Name</TableHead>
                <TableHead>Submission Status</TableHead>
                <TableHead>Grading Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {students.map((student) => (
                <TableRow key={student.id}>
                  <TableCell>{student.name}</TableCell>
                  <TableCell>
                    <Badge variant={student.submission === 'Submitted' ? 'default' : 'destructive'}>
                      {student.submission}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={student.gradingStatus === 'Completed' ? 'default' : 'secondary'}>
                      {student.gradingStatus}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
      
      {/* Grading Status */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Grading Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-4">
            <Clock className="h-8 w-8 text-yellow-500" />
            <div>
              <p className="text-lg font-semibold">Grading in Progress</p>
              <p className="text-gray-600">Estimated completion: 2 hours</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ClassManagementPage;