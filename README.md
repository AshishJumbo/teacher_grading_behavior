## Fariness Analysis of Open Response grading behavior of teachers

------------------

***The logging bug fix was made in as 5pm but just putting it at 7pm the next day out of an abundance of caution '2022-07-11 19:00:00.000 -0400'***


**RCT: 2 X 2 factorial design** 

<table>
    <thead>
        <tr>    
            <th></th>
            <th></th>
            <th colspan="2">Prior Performance</th>
        </tr>
        <tr>    
            <th></th>
            <th></th>
            <th>NO</th>
            <th>YES</th>
        </tr>
    </thead>
    <tbody>
    <tr>
        <td rowspan="2">Student Identity</td>
        <td>Anonymized</td>
        <td>Anonymized with No PP</td>
        <td>Anonymized with PP</td>
    </tr>
    <tr>
        <td>Student Names</td>
        <td>Student Names with No PP</td>
        <td>Student Names with PP</td>
    </tr>
    <tr>
        <td colspan="4"> NOTE: The student Names are fake student names where the teacher can infer the students' <br/> 
                        Ethnicity (Caucasian(3), African American(3), Hispanic(3), Middle Eastern(2), Asian(2), and South Asain(2)) <br/>
                        and Gender (Boy, Girl).</td>
    </tr>
    </tbody>
</table>

**Teacher Category**

Each teacher has 75 responses assigned to them that are divided into 5 sub samples each with 15 responses. 
<br/>
Efforts were made to minimize the total number of ***Open Response Problems*** and have a representative set of scored responses as the Teachers graded the responses on a 5 point scale[0,4].
<table>
    <thead>
        <tr>
            <th>Category</th>
            <th>Description</th>
            <th>Sample Size</th>
            <th>Number of Sub-Samples</th>
            <th>Sub-Sample Size</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>0</td>
            <td>Not Enough Assigned OR. Will get a random sample of teacher grades</td>
            <td>75</td>
            <td>5</td>
            <td>15</td>
        </tr>
        <tr>
            <td>1</td>
            <td>Assigned enough ORs and graded them as well. </td>
            <td>75</td>
            <td>5</td>
            <td>15</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Assigned enough ORs but did not grade enough of them. </td>
            <td>75</td>
            <td>5</td>
            <td>15</td>
        </tr>
    </tbody>
</table>

**Experimental design**

Experimental design pseudocode:
    there at 18 teachers <br/>
    Category 1(7), category 2(4), category 0(7) <br/>
    loop active_batch = 1 to 5: <br/>
    &#09; eligible_batches = [(active_batch)%5, (active_batch+1)%5, (active_batch+2)%5, (active_batch+3)%5]



<table>
    <thead>
        <tr>
            <th>Iteration</th>
            <th>Anonymized</th>
            <th>Student Name</th>
            <th>Anon with Prior Performance</th>
            <th>Student Name with Prior Performance</th>
            <th>Random Sample</th>
            <th>Iteration Batch Size</th>
            <th></th>
            <th>Holdout subsample</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>1-SS(15)</td>
            <td>2-SS(15)</td>
            <td>3-SS(15)</td>
            <td>4-SS(15)</td>
            <td>(20)</td>
            <td>80</td>
            <td></td>
            <td>5-SS(15)</td>
        </tr>
        <tr>
            <td>2</td>
            <td>2-SS(15)</td>
            <td>3-SS(15)</td>
            <td>4-SS(15)</td>
            <td>5-SS(15)</td>
            <td>(20)</td>
            <td>80</td>
            <td></td>
            <td>1-SS(15)</td>
        </tr>
        <tr>
            <td>3</td>
            <td>3-SS(15)</td>
            <td>4-SS(15)</td>
            <td>5-SS(15)</td>
            <td>1-SS(15)</td>
            <td>(20)</td>
            <td>80</td>
            <td></td>
            <td>2-SS(15)</td>
        </tr>
        <tr>
            <td>4</td>
            <td>4-SS(15)</td>
            <td>5-SS(15)</td>
            <td>1-SS(15)</td>
            <td>2-SS(15)</td>
            <td>(20)</td>
            <td>80</td>
            <td></td>
            <td>3-SS(15)</td>
        </tr>
        <tr>
            <td>5</td>
            <td>5-SS(15)</td>
            <td>1-SS(15)</td>
            <td>2-SS(15)</td>
            <td>3-SS(15)</td>
            <td>(20)</td>
            <td>80</td>
            <td></td>
            <td>4-SS(15)</td>
        </tr>
    </tbody>
</table>



